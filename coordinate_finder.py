import pyautogui
import time

def click_to_get_coordinates():
    """Click at desired location to get coordinates"""
    print("Move mouse to desired location and click...")
    print("Starting in 3 seconds...")
    time.sleep(3)
    
    # Get position immediately after this delay
    time.sleep(0.1)  # Small delay to let mouse settle
    x, y = pyautogui.position()
    print(f"Clicked at coordinates: ({x}, {y})")
    return x, y

# Call this function and click where you want
click_to_get_coordinates()