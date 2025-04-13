import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()  # Load .env file
API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
HEADERS = {"x-apikey": API_KEY}

def upload_file(filepath):
    """Uploads a file to VirusTotal and returns an analysis_id if successful."""
    url = "https://www.virustotal.com/api/v3/files"
    with open(filepath, "rb") as f:
        files = {"file": (filepath, f)}
        response = requests.post(url, headers=HEADERS, files=files)

    if response.status_code == 200:
        data = response.json()
        return data["data"]["id"]
    return None

def get_scan_result(analysis_id):
    """Fetches the scan result from VirusTotal using 'analysis_id'."""
    url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
    response = requests.get(url, headers=HEADERS, timeout=15)
    if response.status_code == 200:
        return response.json()["data"]
    return None

def scan_file(filepath):
    """Returns True if file is clean, False if malicious/suspicious or timed out."""
    analysis_id = upload_file(filepath)
    if not analysis_id:
        # Couldn’t upload
        return False

    # Wait 20 seconds to let VirusTotal start scanning
    time.sleep(20)
    start_time = time.time()
    max_wait_seconds = 300  # 5 min

    while True:
        if time.time() - start_time > max_wait_seconds:
            # Timed out, treat as 'malicious' (or unknown)
            return False

        result = get_scan_result(analysis_id)
        if not result:
            # No result yet, wait 10s and try again
            time.sleep(10)
            continue

        status = result["attributes"]["status"]
        if status == "completed":
            stats = result["attributes"]["stats"]
            if stats["malicious"] > 0 or stats["suspicious"] > 0:
                return False
            else:
                return True
        else:
            # "queued" or "running", wait 10s
            time.sleep(10)

def main():
    if not API_KEY:
        print("No VIRUSTOTAL_API_KEY found in .env. Exiting.")
        return

    # Get file path from user
    filepath = input("Enter file path to scan: ").strip()

    # Check if file exists
    if not os.path.isfile(filepath):
        print(f"File not found: {filepath}")
        return

    # Run the scan
    is_clean = scan_file(filepath)
    if is_clean:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    main()
