from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
import logging
from dotenv import load_dotenv


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.g

# Set up your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

#intial fast api
app = FastAPI()


#test items array
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
    

# Define a Pydantic model for the request
class ChatRequest(BaseModel):
    prompt: str
    max_tokens: int = 150
    temperature: float = 0.7

@app.post("/chat")
async def chat_with_openai(request: ChatRequest):
    """
    Endpoint to interact with OpenAI's ChatGPT model using the latest API.
    """
    try:
        # Use the latest OpenAI ChatCompletion API
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",  # or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": request.prompt}
            ],
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        # Extract the response content
        chat_response = response.choices[0].message['content']
        return {"response": chat_response}

    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

# Run the FastAPI server using: uvicorn main:app --reload