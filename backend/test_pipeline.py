import os
import sys
import json
import numpy as np
import pandas as pd
import joblib

# Ensure imports work from backend directory
sys.path.insert(0, os.path.dirname(__file__))

from services.aapa_service import aapa_service
from services.airo_service import execute_action
from utils.simulator import simulator
from utils.audit_log import get_full_log

def run_golden_path_demo():
    print("\n" + "="*50)
    print("PHASE 3: END-TO-END PIPELINE LIVE TEST")
    print("="*50)
    
    # 1. Load the trained Anomaly Engine (Isolation Forest)
    model_path = os.path.join(os.path.dirname(__file__), "ml_models", "isolation_forest_mega.pkl")
    if not os.path.exists(model_path):
        print(f"[ERROR] Anomaly model not found at {model_path}. Did Phase 1 finish?")
        return
        
    print("[1] Loading Anomaly Engine (Isolation Forest)...")
    try:
        model = joblib.load(model_path)
    except Exception as e:
        print(f"[ERROR] Failed to load model: {e}")
        return
        
    # Seed the simulator for the Orchestrator lookup
    simulator._seed_incidents()
    
    # 2. Simulate a live flow record (Anomalous Brute-Force session)
    print("\n[2] Ingesting Live Network Flow Record...")
    flow_features = {
        "duration": 0.5,
        "src_bytes": 50000000.0, # Massive data exfiltration spike
        "dst_bytes": 10.0
    }
    
    X_flow = pd.DataFrame([flow_features])
    X_flow_log = np.log1p(X_flow.astype(float))
    
    # 3. Detection
    is_normal = model.predict(X_flow_log)[0] # 1 for normal, -1 for anomaly
    score_raw = model.decision_function(X_flow_log)[0]
    
    if is_normal == 1:
        print(f" -> Flow scored as BENIGN (Score: {score_raw:.4f}). Pipeline terminates here.")
        return
        
    print(f" -> ANOMALY DETECTED! (Score: {score_raw:.4f})")
    print(f" -> Flow Features: {json.dumps(flow_features)}")
    
    # 4. Attribution (RAG Agent)
    print("\n[3] Triggering AAPA RAG Attribution Agent...")
    entity_payload = {
        "id": "SRV-WEB-001",
        "type": "server",
        "features": flow_features
    }
    alerts_context = [{"description": "Multiple failed SSH logins from single IP followed by large outbound transfer."}]
    
    attribution_result = aapa_service.analyze_entity(entity_payload, alerts_context)
    print(json.dumps(attribution_result, indent=2))
    
    # 5. Orchestration
    print("\n[4] Triggering AIRO Orchestrator...")
    incident_id = "inc-active-01" # Matches CURRENT_INCIDENT seeded in simulator
    
    # Execute a HIGH blast radius action (Network Isolation - action ID 'act_3' in playbook)
    orchestration_result = execute_action(
        incident_id=incident_id,
        action_id="act_3" 
    )
    
    print(f" -> Action Decision: {orchestration_result.get('status', 'Failed')}")
    if orchestration_result.get('status') == "awaiting_approval":
        print(" -> Blast Radius Gate: HIGH severity action requires human approval.")
        
    # 6. Audit Log Check
    print("\n[5] Verifying Immutable Audit Log...")
    log_entries = get_full_log(limit=3)
    for entry_obj in log_entries:
        entry = entry_obj.model_dump() if hasattr(entry_obj, "model_dump") else entry_obj
        if "HIGH" in str(entry.get("action", "")):
            print(f" -> AUDIT ENTRY: [{entry.get('action')}] {entry.get('result')}")
            print(f"    Hash: {entry.get('hash')[:16]}...")
            
    print("\n" + "="*50)
    print("PIPELINE TEST COMPLETE")
    print("="*50 + "\n")

if __name__ == "__main__":
    run_golden_path_demo()
