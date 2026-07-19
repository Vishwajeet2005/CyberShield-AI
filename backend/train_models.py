import os
import joblib
import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from data.mitre_attack import THREAT_ACTORS, ATTACK_TECHNIQUES

def train_bade_model():
    print("Training BADE Isolation Forest model...")
    rng = np.random.RandomState(42)
    # Generate 5000 normal baseline samples (12 features)
    X_train = np.abs(rng.randn(5000, 12))
    # Normalize to 0-1
    X_train = (X_train - X_train.min(0)) / (X_train.max(0) - X_train.min(0) + 1e-9)
    
    model = IsolationForest(n_estimators=150, contamination=0.03, random_state=42)
    model.fit(X_train)
    
    path = os.path.join("ml_models", "bade_iforest.joblib")
    joblib.dump(model, path)
    print(f"BADE model saved to {path}")

def train_aapa_model():
    print("Training AAPA Random Forest classifier...")
    # Build dataset from THREAT_ACTORS
    all_ttps = sorted(ATTACK_TECHNIQUES.keys())
    
    X_train = []
    y_train = []
    
    rng = np.random.RandomState(42)
    
    for actor in THREAT_ACTORS:
        base_vector = np.zeros(len(all_ttps))
        for ttp in actor["ttps"]:
            if ttp in all_ttps:
                base_vector[all_ttps.index(ttp)] = 1.0
                
        # Generate 1000 variations of this actor's TTPs by adding noise (dropping/adding random TTPs)
        for _ in range(1000):
            variation = base_vector.copy()
            # Randomly flip 1-3 bits
            flips = rng.choice(len(all_ttps), size=rng.randint(1, 4), replace=False)
            for f in flips:
                variation[f] = 1.0 - variation[f]
            X_train.append(variation)
            y_train.append(actor["id"])
            
    # Add a "Generic/Unknown" class with random sparse TTPs
    for _ in range(1000):
        variation = np.zeros(len(all_ttps))
        active = rng.choice(len(all_ttps), size=rng.randint(2, 6), replace=False)
        for a in active:
            variation[a] = 1.0
        X_train.append(variation)
        y_train.append("unknown")

    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    
    path = os.path.join("ml_models", "aapa_rf.joblib")
    joblib.dump(model, path)
    print(f"AAPA model saved to {path}")

if __name__ == "__main__":
    os.makedirs("ml_models", exist_ok=True)
    train_bade_model()
    train_aapa_model()
    print("All models trained successfully.")
