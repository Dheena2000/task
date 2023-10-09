import os
from selenium import webdriver
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

# Configuration
URL = "https://dheena.selfmade.fun/"
SCREENSHOT_OLD = "C:\\Users\\DHEENA DHAYALAN\\OneDrive\\Documents\\playground\\cybernets\\screenshots\\screenshot_old.png"
SCREENSHOT_NEW = "C:\\Users\\DHEENA DHAYALAN\\OneDrive\\Documents\\playground\\cybernets\\screenshots\\screenshot_new.png"
HTML_OLD = "C:\\Users\\DHEENA DHAYALAN\\OneDrive\\Documents\\playground\\cybernets\\html\\html_old.html"
HTML_NEW = "C:\\Users\\DHEENA DHAYALAN\\OneDrive\\Documents\\playground\\cybernets\\html\\html_new.html"
EMAIL_USER = "testplayground23@gmail.com"
EMAIL_PASSWORD = "lkjt wkxf gwvn mkin"
RECIPIENT_EMAIL = "dheenadhayalan0625@gmail.com"

# New global variables to keep the previous HTML and screenshot in memory
previous_html = None
previous_screenshot = None

def send_alert():
    print("Sending alert...")
    msg = MIMEText("Changes detected on the website!")
    msg["From"] = EMAIL_USER
    msg["To"] = RECIPIENT_EMAIL
    msg["Subject"] = "Website changes detected"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_USER, RECIPIENT_EMAIL, msg.as_string())
    server.quit()

def capture_data(url):
    print("Capturing data...")
    
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    
    print("Accessing the website...")
    driver.get(url)
    
    # Screenshot
    print("Taking a screenshot...")
    screenshot = driver.get_screenshot_as_png()  # Get screenshot as binary data
    
    # HTML
    print("Fetching and saving HTML...")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    html = str(soup.prettify())
    
    driver.quit()
    print("Data capture complete.")
    
    return screenshot, html

def debug_html_differences(old, new):
    for i, (line_old, line_new) in enumerate(zip(old.splitlines(), new.splitlines())):
        if line_old != line_new:
            print(f"Line {i+1} differs.")
            print("Old:", line_old)
            print("New:", line_new)

# Main Flow
print("Starting the script...")

if not os.path.exists(HTML_OLD) or not os.path.exists(SCREENSHOT_OLD):
    screenshot, html = capture_data(URL)
    
    with open(SCREENSHOT_OLD, "wb") as f:
        f.write(screenshot)
    
    with open(HTML_OLD, "w", encoding="utf-8") as f:
        f.write(html)
    
    print("Data captured for the first time. Run the script again to check for changes.")
else:
    with open(SCREENSHOT_OLD, "rb") as f:
        previous_screenshot = f.read()
    
    with open(HTML_OLD, "r", encoding="utf-8") as f:
        previous_html = f.read()

    current_screenshot, current_html = capture_data(URL)
    
    screenshots_equal = previous_screenshot == current_screenshot
    htmls_equal = previous_html == current_html
    
    if not screenshots_equal or not htmls_equal:
        if not htmls_equal:
            debug_html_differences(previous_html, current_html)
        
        # Update the stored data
        with open(SCREENSHOT_OLD, "wb") as f:
            f.write(current_screenshot)
    
        with open(HTML_OLD, "w", encoding="utf-8") as f:
            f.write(current_html)
        
        send_alert()
        print("Changes detected!")
    else:
        print("No changes detected.")


# This modified version:

#     Keeps the previous screenshot and HTML in memory.
#     Directly compares these with the newly fetched screenshot and HTML without involving any file operations.
#     Prints out the differing lines if any HTML differences are detected.

# By running this version, you should see which exact lines are causing the detected changes. Once we know this, we can refine the solution further.

# This modified approach maintains the state between script runs by saving/loading to/from files. Now, when you run the script multiple times, it should correctly identify changes and maintain its state between runs.