from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os


# Set up your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

#intial fast api
app = FastAPI()

# Define a Pydantic model to handle the request body
class ChatRequest(BaseModel):
    prompt: str
    max_tokens: int = 100

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
    

# Endpoint to interact with ChatGPT
@app.post("/chat")
async def chat_with_gpt(request: ChatRequest):
    try:
        # Send a request to OpenAI's ChatGPT model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": request.prompt}
            ],
            max_tokens=request.max_tokens,
            temperature=0.7
        )
        # Extract the response text
        message = response['choices'][0]['message']['content']
        return {"response": message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

