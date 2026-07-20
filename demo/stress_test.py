import asyncio
import aiohttp
import time
import sys

API_URL = "http://localhost:8000/api/system/demo-trigger"
TARGET_REQUESTS = 500  # Number of incidents to generate

async def trigger_incident(session, req_id):
    try:
        async with session.post(API_URL) as response:
            if response.status == 200:
                data = await response.json()
                sys.stdout.write(f"\r[+] Incident created: {data.get('incident_id')} ({req_id}/{TARGET_REQUESTS})")
                sys.stdout.flush()
                return True
            else:
                return False
    except Exception:
        return False

async def stress_test():
    print("="*60)
    print("🔥 CYBERSHIELD AI - STRESS TEST & LOAD GENERATOR 🔥")
    print("="*60)
    print(f"[*] Target: {API_URL}")
    print(f"[*] Firing {TARGET_REQUESTS} concurrent incident triggers to simulate a massive synchronized APT attack...\n")
    
    start_time = time.time()
    
    # We use aiohttp to send concurrent non-blocking requests
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(1, TARGET_REQUESTS + 1):
            tasks.append(asyncio.create_task(trigger_incident(session, i)))
        
        results = await asyncio.gather(*tasks)
        
    end_time = time.time()
    success_count = sum(1 for r in results if r)
    duration = end_time - start_time
    
    print("\n\n" + "="*60)
    print("✅ STRESS TEST COMPLETE")
    print("="*60)
    print(f"Total Requests  : {TARGET_REQUESTS}")
    print(f"Successful      : {success_count}")
    print(f"Failed          : {TARGET_REQUESTS - success_count}")
    print(f"Time Taken      : {duration:.2f} seconds")
    print(f"Requests/Sec    : {(TARGET_REQUESTS / duration):.2f} req/s")
    print("\n[!] Now go look at the AIRO Dashboard in the UI.")
    print("[!] Check if the React frontend crashes or lags when rendering 500+ critical incidents at once!")

if __name__ == "__main__":
    # Ensure aiohttp is installed
    try:
        import aiohttp
    except ImportError:
        print("[!] Missing aiohttp. Please run: pip install aiohttp")
        sys.exit(1)
        
    asyncio.run(stress_test())
