import os
from selenium import webdriver
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

# Configuration
URL = "https://example.com/"
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
    try:
        print("Capturing data...")

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run Chrome in headless mode
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
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

    except Exception as e:
        print(f"Error during data capture: {e}")
        return None, None

# Main Flow
print("Starting the script...")

if not os.path.exists(HTML_OLD) or not os.path.exists(SCREENSHOT_OLD):
    screenshot, html = capture_data(URL)

    if screenshot and html:
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

    if current_screenshot and current_html:
        screenshots_equal = previous_screenshot == current_screenshot
        htmls_equal = previous_html == current_html

        if not screenshots_equal or not htmls_equal:
            # If desired, add debugging for HTML differences here

            # Update the stored data
            with open(SCREENSHOT_OLD, "wb") as f:
                f.write(current_screenshot)

            with open(HTML_OLD, "w", encoding="utf-8") as f:
                f.write(current_html)

            send_alert()
            print("Changes detected!")
        else:
            print("No changes detected.")
