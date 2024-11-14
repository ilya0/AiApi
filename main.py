from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os

# Set up your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

app = FastAPI()

items = []

##get route to create items
@app.get("/")
def read_root():
    return {" Welcome to AiAPi"}

##post route create items
@app.post("/items")
def create_item(item: str):
    items.append(item)
    return items

@app.get("/items/{item_id}")
def get_item(item_id: int) -> str:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail="Item not found")

