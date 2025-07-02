from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from dotenv import load_dotenv
from typing import Optional
import os
from bson.objectid import ObjectId

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load environment variables and connect to MongoDB
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    raise RuntimeError("MONGO_URI not set in .env file")
try:
    conn = MongoClient(mongo_uri)
    # Test connection
    conn.admin.command('ping')
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    try:
        docs = conn.notes.notes.find({})
        newDocs = []
        for doc in docs:
            newDocs.append({
                "id": str(doc.get("_id")),
                "note": doc.get("note"),
            })
        return templates.TemplateResponse("index.html", {"request": request, "newDocs": newDocs})
    except Exception as e:
        print(f"Error in / endpoint: {e}")
        return HTMLResponse(f"Error fetching notes: {e}", status_code=500)

@app.get("/item/{item_id}")
async def read_items(item_id: str, q: Optional[str] = None):
    try:
        db = conn["notes"]
        doc = db.notes.find_one({"_id": ObjectId(item_id)})
        if doc:
            return {"item_id": item_id, "note": doc.get("note", ""), "q": q}
        return {"error": "Item not found"}
    except Exception as e:
        print(f"Error in /item endpoint: {e}")
        return {"error": str(e)}