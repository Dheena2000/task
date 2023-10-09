import os
from selenium import webdriver
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

# Configuration
URL = "https://www.dheena.selfmade.fun"
SCREENSHOT_OLD ="C:\\Users\\DHEENA DHAYALAN\\OneDrive\\Documents\\playground\\cybernets\\screenshots\\screenshot_old.png"
SCREENSHOT_NEW = "C:\\Users\\DHEENA DHAYALAN\\OneDrive\\Documents\\playground\\cybernets\\screenshots\\screenshot_new.png"
HTML_OLD = "C:\\Users\\DHEENA DHAYALAN\\OneDrive\\Documents\\playground\\cybernets\\html\\html_old.html"
HTML_NEW = "C:\\Users\\DHEENA DHAYALAN\\OneDrive\\Documents\\playground\\cybernets\\html\\html_new.html"
EMAIL_USER = "123176027@sastra.ac.in"
EMAIL_PASSWORD = "Hello2000"
RECIPIENT_EMAIL = "dheenadhayalan0625@gmail.com"

def send_alert():
    msg = MIMEText("Changes detected on the website!")
    msg["From"] = EMAIL_USER
    msg["To"] = RECIPIENT_EMAIL
    msg["Subject"] = "Website changes detected"

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(EMAIL_USER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_USER, RECIPIENT_EMAIL, msg.as_string())
    server.quit()

def capture_data(url, screenshot_path, html_path):
    options = webdriver.ChromeOptions()
    options.headless = True
    chrome_driver_path = r'C:\\chromedriver.exe'
    os.environ["PATH"] += os.pathsep + os.path.dirname(chrome_driver_path)
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.dheena.selfmade.fun")
    
    # Screenshot
    driver.save_screenshot(screenshot_path)
    
    # HTML
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    with open(html_path, "w") as f:
        f.write(str(soup.prettify()))
    
    driver.quit()

# Main Flow
if not os.path.exists(SCREENSHOT_OLD):
    capture_data(URL, SCREENSHOT_OLD, HTML_OLD)
    print("Data captured for the first time. Run the script again to check for changes.")
else:
    capture_data(URL, SCREENSHOT_NEW, HTML_NEW)
    
    # Compare screenshots and HTML
    if (not open(SCREENSHOT_OLD, "rb").read() == open(SCREENSHOT_NEW, "rb").read()) or \
       (not open(HTML_OLD, "r").read() == open(HTML_NEW, "r").read()):
        send_alert()
        print("Changes detected!")

    # Overwrite old data with new data for the next comparison
    os.rename(SCREENSHOT_NEW, SCREENSHOT_OLD)
    os.rename(HTML_NEW, HTML_OLD)
