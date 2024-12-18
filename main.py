import logging
import openai
import os
import sys
import dotenv

from openai import OpenAI
from typing import Union
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

#loading API key from .env
openai.api_key = os.environ.get("OPENAI_API_KEY") 

#Check if the API key is loaded correctly
if not openai.api_key:
    logger.error("OpenAI API key not found. Make sure it's set in the .env file.")
    
#intialize fast api
app = FastAPI()

#### Chat GPT stuff
#chat gpt connection
@app.post("/chat")
async def chat_post(request: Request):
    try:
        body = await request.json()
        message = body.get("message")
        if message:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": message}],
            )
            return JSONResponse({"response": response.choices[0].message.content})
        else:
            return JSONResponse({"error": "Message is required"})
    except Exception as e:
        return JSONResponse({"error": str(e)})
@app.get("/chat")
async def chat_get(request: Request):
    return JSONResponse({"error": "Method Not Allowed"}, status_code=405)
@app.get("/")
async def root(request: Request):
    return JSONResponse({"message": "Welcome to the FastAPI application!"})
