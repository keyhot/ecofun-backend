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

@app.post("/verify")
async def verifyPhoto(user_id: str, binTypeGuess: Bin, file: Annotated[bytes, File()]):
    """
    Veryfies if photo and the selected bin are matching
    """
    def encode_image(image_data):
        return base64.b64encode(image_data).decode('utf-8')

    try:
        image = Image.open(io.BytesIO(file))

        base64_image = encode_image(file)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
            {
                "role": "user",
                "content": [
                {
                    "type": "text",
                    "text": f"Given the image, determine if it is paper, glass, bio, metal/plastic, or mixed? And please provide a short explanation. Make the JSON response as follows: " + "{\"correctBinType\": [ PAPER, GLASS, BIO, METAL_PLASTIC, MIXED ]}, \"notesFromAI\": \"string\""
                },
                {
                    "type": "image_url",
                    "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
                ]
            }
            ],
            "max_tokens": 50
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        choices = response.json().get("choices", [{"message": {"content": "Something went wrong"}}])[0]["message"]["content"]
        ai_response_json = json.loads(choices)
        isBinTypeGuessCorrect = ai_response_json.get("correctBinType", "")[0] == binTypeGuess.value
        print(isBinTypeGuessCorrect, ai_response_json.get("correctBinType", "")[0], binTypeGuess.value)
        pointsEarned = 0
        if isBinTypeGuessCorrect:
            # TODO: Add points to user
            pointsEarned = 10
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
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/gemini")
async def verifyPhoto(user_id: str, binTypeGuess: Bin, photo: UploadFile = File(...)):
    """
    Veryfies if photo and the selected bin are matching
    """
    if not photo.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only images are supported")
    photo = Image.open(photo.file)

    return VerifyPhotoResult(True, 2, "PAPER", "Oh no, your guess was wrong, you should use the PAPER bin.")