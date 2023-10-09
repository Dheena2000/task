import os
from selenium import webdriver
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

# Configuration
URL = "https://unicorn.zeal.lol/"
SCREENSHOT_OLD = "C:\\Users\\DHEENA DHAYALAN\\OneDrive\\Documents\\playground\\cybernets\\screenshots\\screenshot_old.png"
SCREENSHOT_NEW = "C:\\Users\\DHEENA DHAYALAN\\OneDrive\\Documents\\playground\\cybernets\\screenshots\\screenshot_new.png"
HTML_OLD = "C:\\Users\\DHEENA DHAYALAN\\OneDrive\\Documents\\playground\\cybernets\\html\\html_old.html"
HTML_NEW = "C:\\Users\\DHEENA DHAYALAN\\OneDrive\\Documents\\playground\\cybernets\\html\\html_new.html"
EMAIL_USER = "testplayground23@gmail.com"
EMAIL_PASSWORD = "lkjt wkxf gwvn mkin"
RECIPIENT_EMAIL = "dheenadhayalan0625@gmail.com"

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

def capture_data(url, screenshot_path, html_path):
    print("Capturing data...")
    
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    
    print("Accessing the website...")
    driver.get(url)
    
    # Screenshot
    print("Taking a screenshot...")
    driver.save_screenshot(screenshot_path)
    
    # HTML
    print("Fetching and saving HTML...")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    with open(html_path, "w") as f:
        f.write(str(soup.prettify()))
    
    driver.quit()
    print("Data capture complete.")

# Main Flow
print("Starting the script...")
if not os.path.exists(SCREENSHOT_OLD):
    capture_data(URL, SCREENSHOT_OLD, HTML_OLD)
    print("Data captured for the first time. Run the script again to check for changes.")
else:
    capture_data(URL, SCREENSHOT_NEW, HTML_NEW)
    
    # Compare screenshots and HTML
    with open(SCREENSHOT_OLD, "rb") as f1, open(SCREENSHOT_NEW, "rb") as f2:
        screenshots_equal = f1.read() == f2.read()

    with open(HTML_OLD, "r") as f1, open(HTML_NEW, "r") as f2:
        htmls_equal = f1.read() == f2.read()

    if not (screenshots_equal and htmls_equal):
        send_alert()
        print("Changes detected!")
    else:
        print("No changes detected.")

    # Overwrite old data with new data for the next comparison
    if os.path.exists(SCREENSHOT_OLD):
        os.remove(SCREENSHOT_OLD)
    os.rename(SCREENSHOT_NEW, SCREENSHOT_OLD)

    if os.path.exists(HTML_OLD):
        os.remove(HTML_OLD)
    os.rename(HTML_NEW, HTML_OLD)
