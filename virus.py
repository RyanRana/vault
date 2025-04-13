# virus.py
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()  # Load .env file
API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
HEADERS = {"x-apikey": API_KEY}

def upload_file(filepath):
    url = "https://www.virustotal.com/api/v3/files"
    with open(filepath, "rb") as f:
        files = {"file": (filepath, f)}
        response = requests.post(url, headers=HEADERS, files=files)
    if response.status_code == 200:
        data = response.json()
        return data["data"]["id"]
    return None

def get_scan_result(analysis_id):
    url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
    response = requests.get(url, headers=HEADERS, timeout=15)
    if response.status_code == 200:
        return response.json()["data"]
    return None

def scan_file(filepath):
    """Returns True if file is clean, False if malicious/suspicious or timed out."""
    if not API_KEY:
        print("[ERROR] No VIRUSTOTAL_API_KEY in .env")
        return False

    analysis_id = upload_file(filepath)
    if not analysis_id:
        return False

    # Wait 20s to let VirusTotal begin scanning
    time.sleep(20)
    start_time = time.time()
    max_wait_seconds = 300  # 5 min

    while True:
        if time.time() - start_time > max_wait_seconds:
            return False  # Timed out

        result = get_scan_result(analysis_id)
        if not result:
            # No result yet—wait 10s
            time.sleep(10)
            continue

        status = result["attributes"]["status"]
        if status == "completed":
            stats = result["attributes"]["stats"]
            malicious = stats["malicious"]
            suspicious = stats["suspicious"]
            return (malicious == 0 and suspicious == 0)
        else:
            # "queued" or "running"
            time.sleep(10)

# End of virus.py
