from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os
import sys
from dotenv import load_dotenv
import logging
import constants


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

client = OpenAI(
   api_key=os.environ.get("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"),  # This is the default and can be omitted
)

#Check if the API key is loaded correctly
if not openai.api_key:
    logger.error("OpenAI API key not found. Make sure it's set in the .env file.")

#intial fast api
app = FastAPI()


#test items array
items = []

##get route to create items (intial api test)
@app.get("/")
def read_root():
    return {" Welcome to AiAPi"}

##post route create items (intial api test)
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
    
#setting intial vars for ChatGPT
class ChatRequest(BaseModel):
    prompt: str
    max_tokens: int = 150
    temperature: float = 0.7

#chat gpt connection
@app.post("/chat")
async def chat_with_openai(request: ChatRequest):
    """
    Endpoint to interact with OpenAI's ChatGPT model using the new API.
    """
    logger.info(f"Received prompt: {request.prompt}")
    
    try:
        # Using the latest OpenAI API for completions
        response = openai.ChatCompletions.create(
            model="gpt-4-turbo",
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        # Extract the response content
        chat_response = response['choices'][0]['text'].strip()
        logger.info(f"Response: {chat_response}")
        return {"response": chat_response}

    except openai.OpenAIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# Run the FastAPI server using: uvicorn main:app --reload