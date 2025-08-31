from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
import re
import imaplib
import email
import threading
from data import set_data
from scheduler.main import init_jobs
from api import init_application
from concurrent.futures import ThreadPoolExecutor

options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

def get_latest_otp(email_user, email_pass, sender_filter="no-reply@jobs.amazon.com"):
    otp_code = None
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")  # Gmail IMAP
        mail.login(email_user, email_pass)
        mail.select("inbox")

        # Search unread emails from Amazon
        result, data = mail.search(None, f'(UNSEEN FROM "{sender_filter}")')
        if result == "OK":
            for num in data[0].split():
                result, msg_data = mail.fetch(num, "(RFC822)")
                if result != "OK":
                    continue

                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                # Extract OTP (assuming 6-digit code)
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = msg.get_payload(decode=True).decode()

                match = re.search(r"\b(\d{6})\b", body)
                if match:
                    otp_code = match.group(1)
                    print(f"✅ OTP found: {otp_code}")
                    return otp_code

        print("⚠️ No OTP found yet.")
        return None
    except Exception as e:
        print("❌ IMAP error:", e)
        return None


def login(imap_user,imap_pass,driver, email, pin):
    driver.get("https://auth.hiring.amazon.com/#/login")

    time.sleep(2)
    # Select Country
    driver.find_element(By.ID, "country-toggle-button").click()
    driver.find_element(By.XPATH, "//div[contains(text(),'Canada')]").click()
    time.sleep(5)

    # Enter email
    email_input = driver.find_element(By.ID, "login")
    email_input.send_keys(email)
    driver.find_element(By.CSS_SELECTOR, "button[data-test-id='button-continue']").click()
    time.sleep(5)

    pin_input = driver.find_element(By.XPATH, "//input[@type='password']")
    pin_input.send_keys(pin)
    driver.find_element(By.CSS_SELECTOR, "button[data-test-id='button-continue']").click()
    time.sleep(5)

    # Click email verification option
    driver.find_element(By.CSS_SELECTOR, "button[data-test-id='button-submit']").click()
    time.sleep(2)

    otp_code = None
    for _ in range(6):  # retry 6 times, every 10s
        otp_code = get_latest_otp(imap_user, imap_pass)
        if otp_code:
            break
        time.sleep(10)

    if not otp_code:
        raise Exception("❌ OTP not received in time")
    otp_input = driver.find_element(By.ID, "input-test-id-confirmOtp")
    otp_input.send_keys(otp_code)
    driver.find_element(By.CSS_SELECTOR, "button[data-test-id='button-test-id-verifyAccount']").click()
    time.sleep(10)

    cookies = driver.execute_cdp_cmd("Network.getAllCookies", {})
    accessToken = driver.execute_script("return window.localStorage.getItem('accessToken');")

    cookies_header = "; ".join([f"{c['name']}={c['value']}" for c in cookies["cookies"]])

    set_data(cookies=cookies_header, accessToken=accessToken, candidateId=driver.execute_script("return window.localStorage.getItem('bbCandidateId');"))

def update_login_info(driver):
    while True:
        driver.refresh()
        time.sleep(5)
        cookies = driver.execute_cdp_cmd("Network.getAllCookies", {})
        accessToken = driver.execute_script("return window.localStorage.getItem('accessToken');")
        candidateId = driver.execute_script("return window.localStorage.getItem('bbCandidateId');")
        cookies_header = "; ".join([f"{c['name']}={c['value']}" for c in cookies["cookies"]])

        set_data(cookies=cookies_header, accessToken=accessToken, candidateId=candidateId)
        time.sleep(300)

def init():
    driver = webdriver.Chrome(options=options)

    IMAP_USER = "ajass7134@gmail.com"
    IMAP_PASS = "hquededqjstcqqpc"
    start=time.time()
    login(imap_pass=IMAP_PASS,imap_user=IMAP_USER,driver=driver, email="ajass7134@gmail.com", pin="123789")
    print(time.time()-start)

    t1 = threading.Thread(target=update_login_info, args=(driver,))
    t1.start()

    with ThreadPoolExecutor(max_workers=8) as executor:
        while True:
            try:
                jobId, scheduleId = init_jobs()
                if jobId and scheduleId:
                    executor.submit(init_application, jobId=jobId, scheduleId=scheduleId)
            except Exception as e:
                print(f"Error: {e}")

if __name__=="__main__":
    init()