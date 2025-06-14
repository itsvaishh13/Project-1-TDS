
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

from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional, List
import base64
import json

# Load pre-scraped data (Discourse topics)
with open("topics.json", "r", encoding="utf-8") as f:
    discourse_data = json.load(f)

# Define request model
class QuestionRequest(BaseModel):
    question: str
    image: Optional[str] = None

# Define response model
class Link(BaseModel):
    url: str
    text: str

class AnswerResponse(BaseModel):
    answer: str
    links: List[Link]

# Initialize FastAPI
app = FastAPI()

# Dummy semantic search logic (you can replace this later with embeddings or keyword match)
def find_relevant_posts(question: str, data):
    question_lower = question.lower()
    relevant_links = []

    for topic in data.get("topic_list", {}).get("topics", []):
        if any(word in topic['title'].lower() for word in question_lower.split()):
            relevant_links.append({
                "url": f"https://discourse.onlinedegree.iitm.ac.in/t/{topic['slug']}/{topic['id']}",
                "text": topic["title"]
            })
        if len(relevant_links) >= 3:
            break

    return relevant_links

# Endpoint
@app.post("/api/", response_model=AnswerResponse)
async def handle_question(req: QuestionRequest):
    # Step 1: Decode image (if any)
    if req.image:
        try:
            with open("received_image.webp", "wb") as f:
                f.write(base64.b64decode(req.image))
        except Exception as e:
            print(f"Image decode failed: {e}")

    # Step 2: Generate a basic response
    links = find_relevant_posts(req.question, discourse_data)

    # Step 3: Dummy answer (customize later using LLM or rules)
    if links:
        answer = f"I found {len(links)} discussions that might help answer your question."
    else:
        answer = "I couldn’t find relevant discussions based on your question."

    return {
        "answer": answer,
        "links": links
    }

