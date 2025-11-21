import pyautogui
import time
import csv
from datetime import datetime
import os

LOG_FILE = "logs/sms_log.txt"
MESSAGE = "Hello! This is an automated test message."
SCREENSHOTS_DIR = "screenshots"

def log(status, number, details=""):
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {status} - {number} {details}\n")

def find_and_click_element(element_name, confidence=0.8, timeout=10):
    """Find and click an element by screenshot"""
    screenshot_path = os.path.join(SCREENSHOTS_DIR, f"{element_name}.png")
    
    if not os.path.exists(screenshot_path):
        raise FileNotFoundError(f"Screenshot file not found: {screenshot_path}")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(screenshot_path, confidence=confidence)
            if location:
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x, center_y)
                return True
        except pyautogui.ImageNotFoundException:
            pass
        except Exception as e:
            print(f"Error finding {element_name}: {str(e)}")
        
        time.sleep(1)
    
    raise Exception(f"Could not find {element_name} after {timeout} seconds")

def send_sms(number):
    try:
        # Click the new message button (or contact search field)
        find_and_click_element("new_message")
        time.sleep(1)
        
        # Select all and type the phone number
        time.sleep(1)
        pyautogui.hotkey("ctrl", "a")
        pyautogui.typewrite(str(number), interval=0.05)
        time.sleep(1)
        pyautogui.press("enter")
        time.sleep(2)
        
        # Click the message input field
        find_and_click_element("message_box")
        time.sleep(1)
        
        # Type the message
        pyautogui.typewrite(MESSAGE, interval=0.03)
        time.sleep(1)
        
        # Press enter to send
        pyautogui.press("enter")
        
        log("SUCCESS", number)
        print(f"Sent message to {number}")
    except Exception as e:
        log("FAILED", number, str(e))
        print(f"Failed to send message to {number}: {e}")

def main():
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
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