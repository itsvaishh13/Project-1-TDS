from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests
from bs4 import BeautifulSoup

# --- Step 1: Use Selenium to log in manually ---
options = Options()
options.add_argument("--start-maximized")

# Optional: run headless
# options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

print("Launching browser for login...")
driver.get("https://discourse.onlinedegree.iitm.ac.in/login")

# Give user time to log in manually (e.g., SSO login)
input("🔐 After logging in successfully, press Enter here to continue...")

# --- Step 2: Extract cookies from Selenium session ---
cookies = driver.get_cookies()
driver.quit()

# --- Step 3: Use cookies in a requests session ---
session = requests.Session()
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])

# --- Step 4: Fetch the JSON data from the target URL ---
json_url = "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34.json"
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = session.get(json_url, headers=headers)
response.raise_for_status()

data = response.json()
print("\n📚 Topics found:\n")
for topic in data.get("topic_list", {}).get("topics", []):
    print(f"- {topic['title']} (ID: {topic['id']})")


import json

with open("topics.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("✅ Data saved to topics.json")

