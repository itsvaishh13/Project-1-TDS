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

