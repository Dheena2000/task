import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from PIL import Image, ImageChops

# Configurations
URL = "https://www.example.com"
PREVIOUS_SCREENSHOT_PATH = r"C:\Users\DHEENA DHAYALAN\OneDrive\Documents\playground\cybernets\screenshots\previous_screenshot.png"
CURRENT_SCREENSHOT_PATH = r"C:\Users\DHEENA DHAYALAN\OneDrive\Documents\playground\cybernets\screenshots\current_screenshot.png"
PREVIOUS_HTML_PATH = r"C:\Users\DHEENA DHAYALAN\OneDrive\Documents\playground\cybernets\html\previous_html.html"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # usually this is the port for TLS
SMTP_USER = "123176027@sastra.ac.in"
SMTP_PASSWORD = "Hello2000"
RECIPIENT_EMAIL = "dheenadhayalan0625@gmail.com"

def send_email_alert():
    msg = MIMEText("Website content has changed!")
    msg["From"] = SMTP_USER
    msg["To"] = RECIPIENT_EMAIL
    msg["Subject"] = "Website Change Alert"
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USER, SMTP_PASSWORD)
    server.sendmail(SMTP_USER, RECIPIENT_EMAIL, msg.as_string())
    server.quit()

def main():
    # Take a screenshot
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    browser = webdriver.Chrome(executable_path ='C:\chromedriver.exe')
    browser.get(URL)
    browser.save_screenshot(CURRENT_SCREENSHOT_PATH)
    current_html = browser.page_source

    # Check if previous screenshot exists
    try:
        with open(PREVIOUS_SCREENSHOT_PATH, "rb") as f:
            previous_screenshot = Image.open(f)
            current_screenshot = Image.open(CURRENT_SCREENSHOT_PATH)
            diff = ImageChops.difference(previous_screenshot, current_screenshot)
            if diff.getbbox():  # If there's a difference
                send_email_alert()
    except FileNotFoundError:
        pass  # This is the first run, so no previous screenshot to compare

    # Check if previous HTML exists
    try:
        with open(PREVIOUS_HTML_PATH, "r") as f:
            previous_html = f.read()
            if previous_html != current_html:
                send_email_alert()
    except FileNotFoundError:
        pass  # This is the first run, so no previous HTML to compare

    # Save current screenshot and HTML for future comparisons
    with open(PREVIOUS_HTML_PATH, "w") as f:
        f.write(current_html)

    browser.quit()

if __name__ == "__main__":
    main()
