import os
import re
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULT_FOLDER = os.path.join(BASE_DIR, "scraper_result")
RESULT_FILE = os.path.join(BASE_DIR, "scraper_result" ,"results.txt")
IMAGE_DIR = os.path.join(BASE_DIR, "scraper_result" ,"elpais_images")
os.makedirs(IMAGE_DIR, exist_ok=True)

# Clear results.txt and image directory before run
if os.path.exists(RESULT_FILE):
    os.remove(RESULT_FILE)

for filename in os.listdir(IMAGE_DIR):
    file_path = os.path.join(IMAGE_DIR, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)

with open(RESULT_FILE, "w", encoding="utf-8") as f:
    f.write("\u2728 El País Opinion Article Scraper Results\n\n")

# Start Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://elpais.com/opinion/")
driver.maximize_window()

# Accept cookies if the alert appears
try:
    wait = WebDriverWait(driver, 5)
    accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button//span[text()='Accept' or text()='Aceptar']")))
    accept_button.click()
except:
    pass  # No cookie banner

# Wait for articles to load
time.sleep(5)

# Get valid article links (with date in URL)
raw_links = driver.find_elements(By.XPATH, '//a[contains(@href, "/opinion/")]')
article_links = []
for a in raw_links:
    href = a.get_attribute("href")
    if href and re.search(r"/opinion/\d{4}-\d{2}-\d{2}/", href):
        if href not in article_links:
            article_links.append(href)
    if len(article_links) == 5:
        break

# Visit and process each article
for i, link in enumerate(article_links, 1):
    driver.get(link)
    time.sleep(3)

    title = f"[Title not found]"
    content = f"[Content not found]"
    image_path = "[No image found]"

    try:
        title_elem = driver.find_element(By.TAG_NAME, "h1")
        title = title_elem.text.strip()
    except:
        pass

    try:
        paragraphs = driver.find_elements(By.XPATH, '//*[@id="main-content"]/div[2]/p')
        if not paragraphs:
            # Fallback to whole block
            div = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]')
            content = div.text.strip()
        else:
            content = "\n".join(p.text.strip() for p in paragraphs if p.text.strip())
    except:
        content = "[Content not found]"

    try:
        img_elem = driver.find_element(By.XPATH, "//img[contains(@src, 'imagenes.elpais.com/resizer')]")
        img_url = img_elem.get_attribute("src")
        if img_url:
            img_data = requests.get(img_url).content
            image_path = os.path.join(IMAGE_DIR, f"article_{i}.jpg")
            with open(image_path, "wb") as img_file:
                img_file.write(img_data)
    except:
        image_path = "[No image found]"

    # Print & Save result
    result = f"\n\n\U0001F4F0 Article {i}\n"
    result += f"\U0001F4CC Title: {title}\n"
    result += f"\n\U0001F4C4 Content:\n{content}\n"
    result += f"\n\U0001F5BC️ Image Path: {image_path}\n"
    result += f"\n{'='*80}"

    print(result)
    with open(RESULT_FILE, "a", encoding="utf-8") as f:
        f.write(result + "\n")

driver.quit()
