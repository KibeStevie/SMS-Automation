import pyautogui
import time
import csv
from datetime import datetime

LOG_FILE = "logs/sms_log.txt"
MESSAGE = "Hello! This is an automated test message."

def log(status, number, details=""):
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {status} - {number} {details}\n")

def send_sms(number):
    try:
        # Coordinate for new message icon in messaging app
        pyautogui.click(395, 156)
        time.sleep(1)
        pyautogui.hotkey("ctrl", "a")
        pyautogui.typewrite(str(number), interval=0.05)
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(2)
        # Coordinate for send a message input box
        pyautogui.click(753, 1011)
        time.sleep(1)
        pyautogui.typewrite(MESSAGE, interval=0.03)
        time.sleep(1)
        pyautogui.press("enter")
        log("SUCCESS", number)
        print(f"Sent message to {number}")
    except Exception as e:
        log("FAILED", number, str(e))
        print(f"Failed to send message to {number}: {e}")

def main():
    with open("contacts.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if not row:
                continue
            number = row[0].strip()
            if not number.isdigit():
                log("FAILED", number, "(Invalid number)")
                print(f"Invalid number skipped: {number}")
                continue
            send_sms(number)
            time.sleep(3)

if __name__ == "__main__":
    print("Starting SMS automation...")
    time.sleep(3)
    main()