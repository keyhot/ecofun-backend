import io
import httpx
import requests
from fastapi import FastAPI, File, UploadFile, Query, Depends
from fastapi.exceptions import HTTPException
from typing import Annotated
from PIL import Image
from .constants import API_KEY
from .schemas import VerifyPhoto
from .responses import MainScreen, VerifyPhotoResult, Bin
from .database import *
from .routes import users
import app.models as models
from sqlalchemy.orm import Session
from openai import OpenAI
import json
import base64
import logging

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

logger = logging.getLogger(__name__)

app = FastAPI(tags=['EcoFun Main API'])

models.Base.metadata.create_all(bind=engine)
app.include_router(users.router)

client = OpenAI(
    api_key=API_KEY,
)

@app.get("/")
async def root():
    return {"message": "Hello from EcoFun!"}

@app.get("/mainScreen")
async def mainScreen(id: str = Query(...)):
    """
    Returns info about user and tickets to redeem
    """
    return { id, "Kasia Kasia", "2016-08-29T09:12:33.001Z", 1005 }

@app.post("/verify", response_model=VerifyPhotoResult)
async def verifyPhoto(input: VerifyPhoto) -> VerifyPhotoResult:
    """
    Veryfies if photo and the selected bin are matching
    """
    def decode_image(base64_data: str) -> bytes:
        return base64.b64decode(base64_data)

    try:
        # image_data = decode_image(input.file)
        # image = Image.open(io.BytesIO(image_data))

        # Prepare the base64 encoded image for the OpenAI API
        # base64_image = base64.b64encode(image_data).decode('utf-8')
        base64_image = input.file
        
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        print()
        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
            {
                "role": "user",
                "content": [
                {
                    "type": "text",
                    "text": f"Given the image, determine if it is paper, glass, bio, metal/plastic, or mixed? And please provide a short explanation. Make the JSON response as follows, and don't use formatting symbols: " + "{\"correctBinType\": str [ PAPER, GLASS, BIO, METAL_PLASTIC, MIXED ]}, \"notesFromAI\": \"string\""
                },
                {
                    "type": "image_url",
                    "image_url": {
                    "url": f"data:image/jpg;base64,{base64_image}"
                    }
                }
                ]
            }
            ],
            "max_tokens": 50
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        print(response.json())

        logger.info(f"ChatGPT response: {response.json()}")
        choices = response.json().get("choices", [])[0]["message"]["content"]
        logger.info(f"choices: {choices}")
        print('choices', choices)
        isBinTypeGuessCorrect = choices.get("correctBinType", "") == input.binTypeGuess.value
        logger.info(f"isBinTypeGuessCorrect: {isBinTypeGuessCorrect}")
        print(isBinTypeGuessCorrect, choices.get("correctBinType", ""), input.binTypeGuess.value)
        pointsEarned = 0
        print("hello1")
        if isBinTypeGuessCorrect:
            # TODO: Add points to user
            pointsEarned = 10
        print("hello2")
        logger.info(f"Returning Response")
        return {
            "status_code": 200,
            "payload": {
                "isBinTypeGuessCorrect": isBinTypeGuessCorrect,
                "pointsEarned": pointsEarned,
                "correctBinType": ai_response_json.get("correctBinType", ""),
                "notesFromAI": ai_response_json.get("notesFromAI", "")
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e) + "Something went wrong!")

@app.post("/gemini")
async def verifyPhoto(user_id: str, binTypeGuess: Bin, photo: UploadFile = File(...)):
    """
    Veryfies if photo and the selected bin are matching
    """
    if not photo.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only images are supported")
    photo = Image.open(photo.file)

    return VerifyPhotoResult(True, 2, "PAPER", "Oh no, your guess was wrong, you should use the PAPER bin.")