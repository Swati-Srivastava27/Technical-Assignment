from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def wait_for_full_page(driver):
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    time.sleep(1)

def handle_cookie_popup(driver):
    try:
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Accept']]"))
        )
        driver.execute_script("arguments[0].click();", cookie_button)
        print("✅ Accepted cookies.")
        time.sleep(1)
    except:
        print("ℹ️ No cookie alert found or already accepted.")

def check_site_language():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://elpais.com/")
        wait_for_full_page(driver)
        handle_cookie_popup(driver)

        body_text = driver.find_element(By.TAG_NAME, "body").text
        spanish_keywords = ["Noticias", "España", "Política", "Internacional"]

        if any(word in body_text for word in spanish_keywords):
            print("✅ The site is displayed in Spanish.")
        else:
            print("❌ Site may not be in Spanish or could not verify language.")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    check_site_language()
