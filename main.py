# tds_discourse_scraper.py

import requests
import json
import os

# === CONFIG ===
DISCOURSE_BASE_URL = "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34"   # replace if different
CATEGORY_ID = 34                                             # Replace with your TDS category ID
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjEwMDMxODJAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.FazYU0Tm9vCWWA2OkmKRso3YQLwloue6vOy0wZ2DcjM"                               # 🔐 Paste your API key
API_USERNAME = "Vaishnavi"                         # Usually your forum username or "system"
OUTPUT_FILE = "discourse_posts.json"

# === HEADERS ===
HEADERS = {
    "Api-Key": "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjEwMDMxODJAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.FazYU0Tm9vCWWA2OkmKRso3YQLwloue6vOy0wZ2DcjM"
    "

# === FUNCTIONS ===
def get_latest_topics():
    url = f"{DISCOURSE_BASE_URL}/c/{CATEGORY_ID}/l/latest.json"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data.get("topic_list", {}).get("topics", [])

def get_topic_posts(topic_id):
    url = f"{DISCOURSE_BASE_URL}/t/{topic_id}.json"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    topic_data = response.json()
    return topic_data.get("post_stream", {}).get("posts", [])

def scrape_discourse():
    print("🔍 Fetching latest topics...")
    topics = get_latest_topics()
    scraped_data = []

    for topic in topics:
        topic_id = topic["id"]
        title = topic["title"]
        print(f"📘 Scraping Topic: {title}")
        posts = get_topic_posts(topic_id)

        scraped_data.append({
            "topic_id": topic_id,
            "title": title,
            "posts": [{
                "username": post["username"],
                "created_at": post["created_at"],
                "content": post["cooked"]  # HTML formatted
            } for post in posts]
        })

    # Save to JSON file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(scraped_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Scraped data saved to {OUTPUT_FILE}")

# === MAIN ===
if __name__ == "__main__":
    scrape_discourse()
