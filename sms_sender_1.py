import pyautogui      # Library for GUI automation using mouse/keyboard control and image recognition
import time           # For adding delays between automation steps and timeout handling
import csv            # For reading phone numbers from CSV file
from datetime import datetime  # For timestamping log entries
import os             # For file system operations (checking screenshot files, creating directories)

# Configuration constants
LOG_FILE = "logs/sms_log.txt"           # Path to the log file for tracking SMS attempt results
MESSAGE = "Hello! This is an automated test message."  # Default message content to send to all contacts
SCREENSHOTS_DIR = "screenshots"         # Directory containing UI element screenshots for image recognition

def log(status, number, details=""):
    """
    Write SMS attempt results to a log file with timestamp for audit and debugging purposes.
    
    Args:
        status (str): "SUCCESS" or "FAILED" indicating the outcome
        number (str): Phone number that was attempted
        details (str): Optional additional information (error message, validation notes, etc.)
    
    The log file is opened in append mode to preserve previous entries across script runs.
    """
    with open(LOG_FILE, "a") as f:  # Open log file in append mode
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format current time as string
        f.write(f"[{timestamp}] {status} - {number} {details}\n")  # Write formatted log entry

def find_and_click_element(element_name, confidence=0.8, timeout=10):
    """
    Locate a UI element on screen using image recognition and click its center.
    This is the core function that enables resolution-independent automation.
    
    Args:
        element_name (str): Name of the screenshot file (without .png extension)
        confidence (float): Minimum match confidence (0.0-1.0) for image recognition
                           Requires OpenCV installation for this parameter to work
        timeout (int): Maximum time in seconds to keep searching for the element
    
    Returns:
        bool: True if element was found and clicked successfully
        
    Raises:
        FileNotFoundError: If the specified screenshot file doesn't exist
        Exception: If element is not found within the timeout period
        
    Note: This approach is more robust than hardcoded coordinates as it works across
    different screen resolutions and minor UI changes.
    """
    # Construct full path to the screenshot file
    screenshot_path = os.path.join(SCREENSHOTS_DIR, f"{element_name}.png")
    
    # Verify screenshot file exists before attempting to use it
    if not os.path.exists(screenshot_path):
        raise FileNotFoundError(f"Screenshot file not found: {screenshot_path}")
    
    # Start timer for timeout handling
    start_time = time.time()
    
    # Keep searching for the element until timeout is reached
    while time.time() - start_time < timeout:
        try:
            # Search entire screen for the screenshot pattern with specified confidence
            location = pyautogui.locateOnScreen(screenshot_path, confidence=confidence)
            if location:
                # Calculate center coordinates of found element
                center_x, center_y = pyautogui.center(location)
                # Click at the center of the found element
                pyautogui.click(center_x, center_y)
                return True  # Successfully found and clicked
        except pyautogui.ImageNotFoundException:
            # Element not found on screen - continue searching
            pass
        except Exception as e:
            # Handle unexpected errors during image recognition
            print(f"Error finding {element_name}: {str(e)}")
        
        # Wait 1 second before next search attempt to avoid excessive CPU usage
        time.sleep(1)
    
    # Timeout reached - element was not found
    raise Exception(f"Could not find {element_name} after {timeout} seconds")

def send_sms(number):
    """
    Send an SMS to a single phone number using Microsoft Phone Link with screenshot-based automation.
    This function simulates human interaction with the Phone Link interface using visual recognition.
    
    Args:
        number (str): Phone number to send SMS to
        
    Workflow:
        1. Click "New Message" button using screenshot recognition
        2. Enter phone number in contact field
        3. Confirm contact selection
        4. Click message input field using screenshot recognition
        5. Type and send message
        
    Note: This implementation is more reliable than coordinate-based automation as it
    adapts to different screen resolutions and minor UI layout changes.
    """
    try:
        # Step 1: Click the "New Message" button using screenshot recognition
        # Looks for "screenshots/new_message.png" on screen
        find_and_click_element("new_message")
        time.sleep(1)  # Allow UI to respond to click
        
        # Step 2: Clear existing text and enter the phone number
        time.sleep(1)  # Additional delay for UI stability
        pyautogui.hotkey("ctrl", "a")  # Select any existing text in the field
        pyautogui.typewrite(str(number), interval=0.05)  # Type phone number with small delay between keystrokes
        time.sleep(1)  # Wait for contact lookup/suggestion
        pyautogui.press("enter")  # Confirm contact selection
        time.sleep(2)  # Wait for message composition screen to load
        
        # Step 3: Click the message input field using screenshot recognition
        # Looks for "screenshots/message_box.png" on screen
        find_and_click_element("message_box")
        time.sleep(1)  # Allow text field to become focused
        
        # Step 4: Type the message content and send
        pyautogui.typewrite(MESSAGE, interval=0.03)  # Type message with small delay between characters
        time.sleep(1)  # Brief pause before sending
        pyautogui.press("enter")  # Press Enter to send the SMS
        
        # Step 5: Log successful transmission
        log("SUCCESS", number)
        print(f"Sent message to {number}")
        
    except Exception as e:
        # Handle any errors during the automation process
        log("FAILED", number, str(e))
        print(f"Failed to send message to {number}: {e}")

def main():
    """
    Main orchestration function that processes contacts from CSV and sends SMS messages.
    Handles file operations, input validation, and coordinates the automation workflow.
    
    Features:
        - Creates log directory if it doesn't exist
        - Reads phone numbers from contacts.csv
        - Validates phone numbers (digits only)
        - Processes each number with appropriate delays
        - Handles errors gracefully with logging
    """
    # Ensure logs directory exists to prevent file write errors
    os.makedirs("logs", exist_ok=True)
    
    # Open and read contacts from CSV file
    with open("contacts.csv", "r") as file:
        reader = csv.reader(file)  # Create CSV reader object
        for row in reader:  # Process each row in the CSV file
            if not row:  # Skip empty rows
                continue
            number = row[0].strip()  # Extract and clean phone number from first column
            
            # Validate phone number format (must contain only digits)
            if not number.isdigit():
                log("FAILED", number, "(Invalid number)")
                print(f"Invalid number skipped: {number}")
                continue
                
            # Send SMS to validated phone number
            send_sms(number)
            time.sleep(3)  # Wait 3 seconds between messages to prevent spam detection and UI overload

if __name__ == "__main__":
    """
    Script entry point.
    Provides user notification and preparation time before automation begins.
    
    The 3-second delay gives the user time to:
        - Ensure Microsoft Phone Link is open and visible
        - Focus the Phone Link window
        - Prepare their screen for automation
    """
    print("Starting SMS automation...")
    print("Make sure Microsoft Phone Link is open, connected, and visible on your screen!")
    time.sleep(3)  # 3-second countdown before starting automation
    main()  # Execute the main automation workflow