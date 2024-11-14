from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv


# Set up your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

#intial fast api
app = FastAPI()

# Define a Pydantic model for request data
class ChatRequest(BaseModel):
    prompt: str
    max_tokens: int = 150
    temperature: float = 0.7


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
    



@app.post("/chat")
async def chat_with_openai(request: ChatRequest):
    """
    Endpoint to interact with OpenAI's GPT model.
    """
    try:
        # Use the latest ChatCompletion API
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": request.prompt}
            ],
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )

        # Extract the response content
        chat_response = response.choices[0].message['content'].strip()
        return {"response": chat_response}

    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

# Run the FastAPI server using: uvicorn main:app --reload