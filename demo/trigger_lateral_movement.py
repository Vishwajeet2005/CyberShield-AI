import time
import sys
import random

def print_typewriter(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def simulate_attack():
    print("\n" + "="*70)
    print("🚀 CYBERSHIELD AI - LIVE DEMO SCENARIO: APT41 LATERAL MOVEMENT")
    print("="*70 + "\n")
    
    time.sleep(1)
    print_typewriter("[*] Initializing Kafka Event Stream to BADE (Anomaly Engine)...")
    time.sleep(0.5)
    
    print_typewriter("\n[+] INGESTING ENDPOINT TELEMETRY (AIIMS-DC-01)...")
    for i in range(1, 6):
        print(f"    -> [OK] Process Creation Event: C:\\Windows\\System32\\svchost.exe (PID: {random.randint(1000, 9000)})")
        time.sleep(0.2)
    
    print_typewriter("\n[!] DETECTED SUSPICIOUS POWERSHELL EXECUTION...")
    print("    -> Command: powershell.exe -nop -w hidden -EncodedCommand JABzAD0ATgBlAHcALQBP...")
    time.sleep(1)
    
    print_typewriter("\n[*] BADE: Analyzing 12-dimensional feature vector against 30-day baseline...")
    time.sleep(1)
    print_typewriter("    [WARNING] DEVIATION SCORE: 87/100 (Threshold: 70)")
    
    print_typewriter("\n[+] DETECTING LATERAL MOVEMENT (SMB Port 445)...")
    for target in ["10.0.4.15", "10.0.4.22", "10.0.4.89"]:
        print(f"    -> Connection attempt to {target}:445 [SUCCESS]")
        time.sleep(0.3)
        
    print_typewriter("\n[*] TRIGGERING AAPA (APT Attribution & Prediction Agent)...")
    time.sleep(1)
    print_typewriter("    -> Matching TTPs against MITRE ATT&CK Knowledge Graph...")
    time.sleep(0.5)
    print("       - T1059.001 (PowerShell)")
    print("       - T1021.002 (SMB/Windows Admin Shares)")
    print("       - T1078 (Valid Accounts)")
    
    print_typewriter("\n[!] ATTRIBUTION COMPLETE:")
    print_typewriter("    -> THREAT ACTOR: APT41 (China)")
    print_typewriter("    -> CONFIDENCE: 91%")
    
    print_typewriter("\n[*] AIRO: Generating Containment Playbook...")
    time.sleep(1)
    print_typewriter("    -> Action 1: Isolate compromised endpoint (AIIMS-DC-01) [BLAST RADIUS: HIGH]")
    print_typewriter("    -> Action 2: Block egress C2 IP (185.11.12.X) [BLAST RADIUS: LOW]")
    print_typewriter("    -> Action 3: Revoke compromised user tokens [BLAST RADIUS: MEDIUM]")
    
    print_typewriter("\n[*] ALERT PUSHED TO CYBERSHIELD AI DASHBOARD.")
    print("\n" + "="*70)
    print("✅ DEMO TRIGGER COMPLETE. PLEASE CHECK THE AIRO PLAYBOOK DASHBOARD.")
    print("="*70 + "\n")

if __name__ == "__main__":
    try:
        simulate_attack()
    except KeyboardInterrupt:
        print("\n[!] DEMO ABORTED.")
