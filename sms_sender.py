import pyautogui      # Library for GUI automation (mouse/keyboard control)
import time           # For adding delays between automation steps
import csv            # For reading phone numbers from CSV file
from datetime import datetime  # For timestamping log entries

# Configuration constants
LOG_FILE = "logs/sms_log.txt"           # Path to the log file for tracking SMS attempts
MESSAGE = "Hello! This is an automated test message."  # Default message to send to all contacts

def log(status, number, details=""):
    """
    Log SMS attempt results to a file with timestamp.
    
    Args:
        status (str): "SUCCESS" or "FAILED"
        number (str): Phone number that was attempted
        details (str): Optional error message or additional information
    """
    with open(LOG_FILE, "a") as f:  # Open log file in append mode
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current timestamp
        f.write(f"[{timestamp}] {status} - {number} {details}\n")  # Write formatted log entry

def send_sms(number):
    """
    Send an SMS to a single phone number using Microsoft Phone Link UI automation.
    This function simulates the exact steps a human would take in the Phone Link app.
    
    Args:
        number (str): Phone number to send SMS to
    
    Note: Coordinates are hardcoded for a specific screen resolution (1920x1080).
    This approach is fragile and will break if screen resolution or UI changes.
    """
    try:
        # Step 1: Click the "New Message" button in Phone Link
        # Coordinates (395, 156) target the new message icon
        pyautogui.click(395, 156)
        time.sleep(1)  # Wait for UI to respond
        
        # Step 2: Clear any existing text and enter the phone number
        pyautogui.hotkey("ctrl", "a")  # Select all existing text
        pyautogui.typewrite(str(number), interval=0.05)  # Type phone number with small delay between keystrokes
        time.sleep(1)  # Allow time for contact lookup
        
        # Step 3: Confirm the contact selection
        pyautogui.press("enter")  # Press Enter to select the contact
        time.sleep(2)  # Wait for message composition screen to load
        
        # Step 4: Click the message input field to focus it
        # Coordinates (753, 1011) target the message text area
        pyautogui.click(753, 1011)
        time.sleep(1)  # Wait for field to be ready
        
        # Step 5: Type and send the message
        pyautogui.typewrite(MESSAGE, interval=0.03)  # Type message content
        time.sleep(1)  # Brief pause before sending
        pyautogui.press("enter")  # Press Enter to send the SMS
        
        # Step 6: Log successful transmission
        log("SUCCESS", number)
        print(f"Sent message to {number}")
        
    except Exception as e:
        # Handle any errors during the automation process
        log("FAILED", number, str(e))
        print(f"Failed to send message to {number}: {e}")

def main():
    """
    Main function: Reads phone numbers from CSV file and sends SMS to each valid number.
    Includes basic input validation and error handling for invalid phone numbers.
    """
    with open("contacts.csv", "r") as file:  # Open contacts file
        reader = csv.reader(file)  # Create CSV reader object
        for row in reader:  # Iterate through each row in the CSV
            if not row:  # Skip empty rows
                continue
            number = row[0].strip()  # Extract and clean the phone number (first column)
            
            # Validate phone number (must contain only digits)
            if not number.isdigit():
                log("FAILED", number, "(Invalid number)")
                print(f"Invalid number skipped: {number}")
                continue
                
            # Send SMS to valid number
            send_sms(number)
            time.sleep(3)  # Wait 3 seconds between messages to avoid spam detection or UI overload

if __name__ == "__main__":
    """
    Entry point of the script.
    Provides a 3-second countdown to allow user to prepare the Phone Link window.
    """
    print("Starting SMS automation...")
    print("Make sure Microsoft Phone Link is open and visible on your screen!")
    time.sleep(3)  # Give user time to focus Phone Link window
    main()  # Execute main automation logic