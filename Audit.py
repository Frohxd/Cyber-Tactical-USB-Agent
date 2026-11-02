import psutil
import socket
import platform
import sys
import time
import requests
import ctypes

API_URL = "YOUR_TARGET_URL" 
TOKEN = "YOUR_API_TOKEN"

def get_exact_os():
    if platform.system() == "Windows":
        build_number = int(platform.version().split('.')[-1])
        if build_number >= 22000:
            return f"Windows 11"
        else:
            return f"Windows 10"
    return f"{platform.system()} {platform.release()}"

def get_free_disk_gb():
    if platform.system() == "Windows":
        try:
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                ctypes.c_wchar_p("C:\\"),
                None,
                None,
                ctypes.pointer(free_bytes)
            )
            return round(free_bytes.value / (1024**3), 2)
        except Exception:
            return 0.0
    else:
        try:
            return round(psutil.disk_usage('/').free / (1024**3), 2)
        except Exception:
            return 0.0

def collect_and_send():
    psutil.cpu_percent(interval=None)
    time.sleep(0.5)  

    data = {
        "hostname": socket.gethostname(),
        "os": get_exact_os(),
        "ip_address": socket.gethostbyname(socket.gethostname()),
        "cpu_usage": psutil.cpu_percent(interval=None),
        "ram_usage": psutil.virtual_memory().percent,
        "disk_free_gb": get_free_disk_gb() 
    }

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        res = requests.post(API_URL, json=data, headers=headers)
        if res.status_code == 200:
            print("[SUCCESS] The data was recieved!")
        else:
            print(f"[-] Server error: {res.status_code} - {res.text}")
    except Exception as e:
        print("[-] Error while connecting to the server:", e)

if __name__ == "__main__":
    collect_and_send()