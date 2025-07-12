import time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By

USERNAME = "swatisrivastava_fzG7AI"
ACCESS_KEY = "WAxSVqGaqhsDqUuYuCTX"
BROWSERSTACK_URL = f"https://{USERNAME}:{ACCESS_KEY}@hub.browserstack.com/wd/hub"

# Browser configurations (desktop and mobile)
browsers = [
    # Desktop 1
    {
        "browserName": "Chrome",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "11",
            "sessionName": "Chrome Win Test"
        }
    },
    # Desktop 2
    {
        "browserName": "Firefox",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "10",
            "sessionName": "Firefox Win Test"
        }
    },
    # Desktop 3
    {
        "browserName": "Safari",
        "bstack:options": {
            "os": "OS X",
            "osVersion": "Monterey",
            "sessionName": "Safari Mac Test"
        }
    },
    # Mobile 1
    {
        "browserName": "Chrome",
        "bstack:options": {
            "deviceName": "Samsung Galaxy S22",
            "osVersion": "12.0",
            "realMobile": True,
            "sessionName": "Galaxy S22 Test"
        }
    },
    # Mobile 2
    {
        "browserName": "Safari",
        "bstack:options": {
            "deviceName": "iPhone 13",
            "osVersion": "15.0",
            "realMobile": True,
            "sessionName": "iPhone 13 Test"
        }
    }
]

def run_test(cap_dict):
    try:
        browser_name = cap_dict.get("browserName")
        bstack_options = cap_dict.get("bstack:options")

        options = webdriver.ChromeOptions()
        options.set_capability("browserName", browser_name)
        options.set_capability("bstack:options", bstack_options)

        driver = webdriver.Remote(
            command_executor=BROWSERSTACK_URL,
            options=options
        )

        driver.get("https://elpais.com/opinion/editoriales/")
        time.sleep(5)

        try:
            title = driver.find_element(By.TAG_NAME, "h1").text
            print(f"✅ {bstack_options['sessionName']}: {title}")
        except Exception as e:
            print(f"❌ {bstack_options['sessionName']}: Could not get title - {e}")
        driver.quit()

    except Exception as e:
        print(f"❌ {cap_dict['bstack:options'].get('sessionName', 'Unnamed')}: Failed to run session - {e}")

# Run all tests in parallel
threads = []
for caps in browsers:
    t = threading.Thread(target=run_test, args=(caps,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
