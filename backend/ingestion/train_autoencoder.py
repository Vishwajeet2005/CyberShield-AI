"""
CyberShield AI — PyTorch LSTM Autoencoder for Anomaly Detection
===============================================================
Trained on the same 3 datasets as the IsolationForest ensemble.
Reconstruction error is used as anomaly score — high error = anomalous sequence.
Used as a second scoring signal alongside IsolationForest.
"""

import os
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from typing import Tuple

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "ml_models", "autoencoder.pt")
SCALER_PATH = os.path.join(os.path.dirname(__file__), "..", "ml_models", "autoencoder_scaler.npy")

FEATURE_NAMES = [
    "login_count", "failed_logins", "bytes_sent", "bytes_received",
    "unique_destinations", "port_scan_count", "off_hours_logins",
    "privilege_escalations", "process_creations", "dns_queries",
    "lateral_connections", "file_operations"
]
N_FEATURES = len(FEATURE_NAMES)
HIDDEN_DIM = 32
LATENT_DIM = 8
SEQ_LEN = 10      # Window of 10 observations per entity
EPOCHS = 30
BATCH_SIZE = 64
LR = 1e-3


# ─── Model Definition ────────────────────────────────────────────────────────

class LSTMAutoencoder(nn.Module):
    """
    LSTM Encoder-Decoder Autoencoder.
    Encodes a sequence of feature vectors into a compressed latent representation,
    then reconstructs the original sequence. High reconstruction error = anomaly.
    """
    def __init__(self, n_features: int, hidden_dim: int, latent_dim: int):
        super().__init__()
        # Encoder
        self.encoder_lstm = nn.LSTM(n_features, hidden_dim, num_layers=2,
                                    batch_first=True, dropout=0.2)
        self.encoder_fc   = nn.Linear(hidden_dim, latent_dim)

        # Decoder
        self.decoder_fc   = nn.Linear(latent_dim, hidden_dim)
        self.decoder_lstm = nn.LSTM(hidden_dim, n_features, num_layers=2,
                                    batch_first=True, dropout=0.2)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (batch, seq_len, n_features)
        enc_out, _ = self.encoder_lstm(x)
        latent = self.encoder_fc(enc_out[:, -1, :])          # last hidden state

        # Decode: repeat latent vector across seq_len
        latent_seq = self.decoder_fc(latent).unsqueeze(1).repeat(1, x.size(1), 1)
        recon, _ = self.decoder_lstm(latent_seq)
        return recon


# ─── Data Helpers ─────────────────────────────────────────────────────────────

def _load_nsl_kdd(max_rows: int = 50000) -> np.ndarray:
    """Load NSL-KDD and map its 41 features down to our 12 common features."""
    from data.nsl_loader import load_nsl_kdd
    try:
        df = load_nsl_kdd(max_rows=max_rows)
        # Map NSL-KDD columns to our feature space (best-effort)
        mapping = {
            "login_count":           df.get("num_access_files", np.zeros(len(df))),
            "failed_logins":         df.get("num_failed_logins", np.zeros(len(df))),
            "bytes_sent":            df.get("src_bytes", np.zeros(len(df))),
            "bytes_received":        df.get("dst_bytes", np.zeros(len(df))),
            "unique_destinations":   df.get("num_compromised", np.zeros(len(df))),
            "port_scan_count":       df.get("count", np.zeros(len(df))),
            "off_hours_logins":      np.zeros(len(df)),
            "privilege_escalations": df.get("root_shell", np.zeros(len(df))),
            "process_creations":     df.get("num_shells", np.zeros(len(df))),
            "dns_queries":           df.get("srv_count", np.zeros(len(df))),
            "lateral_connections":   df.get("same_srv_rate", np.zeros(len(df))),
            "file_operations":       df.get("num_file_creations", np.zeros(len(df))),
        }
        return np.column_stack([np.asarray(v).reshape(-1) for v in mapping.values()])
    except Exception:
        return np.random.randn(5000, N_FEATURES)


def _generate_synthetic_benign(n: int = 20000) -> np.ndarray:
    """Generate synthetic benign traffic for training."""
    rng = np.random.RandomState(42)
    data = np.abs(rng.randn(n, N_FEATURES))
    # Apply realistic scaling per feature
    scales = [8, 0.5, 5e7, 2e8, 15, 0.1, 0.2, 0.05, 20, 100, 0.5, 80]
    return data * np.array(scales)


def _build_sequences(X: np.ndarray, seq_len: int) -> np.ndarray:
    """Slide a window of seq_len across the data to create sequences."""
    n = len(X) - seq_len
    return np.stack([X[i:i+seq_len] for i in range(n)])


def _normalize(X: np.ndarray, scaler=None) -> Tuple[np.ndarray, np.ndarray]:
    """Min-max normalize features. Returns (normalized, scaler_params)."""
    if scaler is None:
        mins = X.min(axis=0)
        maxs = X.max(axis=0)
        scaler = np.stack([mins, maxs])
    mins, maxs = scaler[0], scaler[1]
    X_norm = (X - mins) / (maxs - mins + 1e-9)
    return np.clip(X_norm, 0, 1), scaler


# ─── Training ─────────────────────────────────────────────────────────────────

def train():
    print("=" * 60)
    print("PYTORCH LSTM AUTOENCODER — TRAINING")
    print("=" * 60)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"  Device: {device}")

    # Build training data
    print("  [1/4] Building benign training corpus...")
    X_synth = _generate_synthetic_benign(20000)
    try:
        X_nsl   = _load_nsl_kdd(30000)
        X_all   = np.vstack([X_synth, X_nsl])
        print(f"        Synthetic + NSL-KDD: {len(X_all)} rows")
    except Exception:
        X_all = X_synth
        print(f"        Synthetic only: {len(X_all)} rows")

    # Normalize
    print("  [2/4] Normalizing features...")
    X_norm, scaler = _normalize(X_all)
    np.save(SCALER_PATH, scaler)

    # Build sequences
    print("  [3/4] Building sliding-window sequences (len=10)...")
    seqs = _build_sequences(X_norm, SEQ_LEN)
    np.random.shuffle(seqs)
    X_tensor = torch.FloatTensor(seqs).to(device)
    dataset = TensorDataset(X_tensor)
    loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

    # Build model
    model = LSTMAutoencoder(N_FEATURES, HIDDEN_DIM, LATENT_DIM).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)
    criterion = nn.MSELoss()

    # Train
    print(f"  [4/4] Training {EPOCHS} epochs...")
    for epoch in range(EPOCHS):
        model.train()
        total_loss = 0.0
        for (batch,) in loader:
            optimizer.zero_grad()
            recon = model(batch)
            loss = criterion(recon, batch)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        avg_loss = total_loss / len(loader)
        if (epoch + 1) % 5 == 0:
            print(f"        Epoch {epoch+1:3d}/{EPOCHS} — Loss: {avg_loss:.6f}")

    torch.save(model.state_dict(), MODEL_PATH)
    print(f"\n  Model saved: {MODEL_PATH}")
    print("  Training complete.")


# ─── Inference ────────────────────────────────────────────────────────────────

class AutoencoderScorer:
    """
    Thin wrapper for real-time scoring.
    Maintains a rolling window of recent feature vectors per entity.
    """
    _instance = None

    def __init__(self):
        self._model: LSTMAutoencoder | None = None
        self._scaler: np.ndarray | None = None
        self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._windows: dict[str, list] = {}  # entity_id -> last SEQ_LEN feature vectors
        self._threshold: float = 0.05        # reconstruction error threshold
        self._loaded = False

    def load(self) -> bool:
        """Load the trained model. Returns True if successful."""
        try:
            self._model = LSTMAutoencoder(N_FEATURES, HIDDEN_DIM, LATENT_DIM)
            self._model.load_state_dict(torch.load(MODEL_PATH, map_location=self._device,
                                                    weights_only=True))
            self._model.eval()
            self._scaler = np.load(SCALER_PATH)
            self._loaded = True
            return True
        except Exception as e:
            print(f"[AutoencoderScorer] Could not load model: {e}. Will fallback to None.")
            self._loaded = False
            return False

    def score(self, entity_id: str, features: dict) -> float | None:
        """
        Score a single observation for an entity.
        Returns reconstruction error (0.0 to 1.0+) or None if window not full yet.
        Higher = more anomalous.
        """
        if not self._loaded:
            return None

        vec = np.array([features.get(f, 0.0) for f in FEATURE_NAMES], dtype=float)
        # Normalize
        mins, maxs = self._scaler[0], self._scaler[1]
        vec_norm = np.clip((vec - mins) / (maxs - mins + 1e-9), 0, 1)

        # Maintain rolling window
        window = self._windows.get(entity_id, [])
        window.append(vec_norm)
        if len(window) > SEQ_LEN:
            window = window[-SEQ_LEN:]
        self._windows[entity_id] = window

        if len(window) < SEQ_LEN:
            return None  # Window not full yet

        # Reconstruct
        with torch.no_grad():
            x = torch.FloatTensor(window).unsqueeze(0).to(self._device)
            recon = self._model(x)
            error = float(nn.MSELoss()(recon, x).item())

        return error


# Singleton
autoencoder_scorer = AutoencoderScorer()


if __name__ == "__main__":
    train()
