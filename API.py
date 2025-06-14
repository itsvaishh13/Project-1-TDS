from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Setup headless Chrome
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

# Visit the course site
driver.get("https://tds.s-anand.net/#/2025-01/")
time.sleep(5)  # wait for JS to load

# Extract content (modify based on structure)
page_source = driver.page_source
with open("course_content.html", "w", encoding="utf-8") as f:
    f.write(page_source)

print("✅ Course content saved as course_content.html")

driver.quit()
