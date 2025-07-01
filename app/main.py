from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from app.database import user1

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

conn = MongoClient(user1)

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    """
    Render the index page with the provided id.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/item/{id}")
def read_items(item_id: int, q: str | None = None):
    """
    Retrieve an item by its ID, with an optional query parameter.
    """
    return {"item_id": item_id, "q": q}