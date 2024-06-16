import io
import httpx
import requests
from fastapi import FastAPI, File, UploadFile, Query, Depends
from fastapi.exceptions import HTTPException
from typing import Annotated
from PIL import Image
from .constants import API_KEY, IS_PROD
from .schemas import VerifyPhoto
from .responses import MainScreen, VerifyPhotoPayload, VerifyPhotoResult, Bin, MainScreen
from .helpers import update_or_create_user_score, get_marketplaces, get_user_by_id, get_marketplace_by_id
from .database import engine, get_db
from .routes import users, marketplaces
import app.models as models
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from openai import OpenAI
import json
import base64
import logging

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

logger = logging.getLogger(__name__)

app = FastAPI(tags=['EcoFun Main API'])

models.Base.metadata.create_all(bind=engine)
if not IS_PROD:
    app.include_router(users.router)
    app.include_router(marketplaces.router)


client = OpenAI(
    api_key=API_KEY,
)

@app.get("/")
async def root():
    return {"message": "Hello from EcoFun!"}

@app.post("/claim")
async def claimTicket(user_id: str = Query(...), mplace_id: int = Query(...), db: Session = Depends(get_db)):
    """
    Claims a ticket
    """
    marketplace = get_marketplace_by_id(mplace_id, db)
    price = marketplace["price"]
    update_or_create_user_score(user_id, -price, db)
    return {"message": "Ticket claimed!"}

@app.get("/mainScreen", response_model=MainScreen)
async def mainScreen(id: str = Query(...), db: Session = Depends(get_db)):
    """
    Returns info about user and tickets to redeem
    """
    update_or_create_user_score(id, 0, db)
    logger.info("Requesting marketplaces")
    marketplaces = get_marketplaces(db)
    marketplaces = [marketplace.as_dict() for marketplace in marketplaces]
    logger.info("Requesting user info")
    user = get_user_by_id(id, db)
    logger.info("Returning response")
    response = MainScreen(
        id=id,
        marketplaces=marketplaces,
        pointsAmount=user["score"]
    )
    return response

@app.post("/verify", response_model=VerifyPhotoResult)
async def verifyPhoto(input: VerifyPhoto, db: Session = Depends(get_db)) -> VerifyPhotoResult:
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
        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
            {
                "role": "user",
                "content": [
                {
                    "type": "text",
                    "text": f"Given the image, determine in which bin I should put it into: paper, glass, bio, metal/plastic, or mixed? And please provide a very short explanation. Make the JSON response is exactly as follows, and do not use formatting symbols: " + "{\"correctBinType\": str [ PAPER, GLASS, BIO, METAL_PLASTIC, MIXED ]}, \"notesFromAI\": \"string\"}"
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
            "max_tokens": 200
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        print(response.json())

        logger.info(f"ChatGPT response: {response.json()}")
        choices = response.json().get("choices", [])[0]["message"]["content"]
        logger.info(f"choices: {choices}")
        ai_response_json = json.loads(choices)
        logger.info(f"ai_response_json: {ai_response_json}")

        isBinTypeGuessCorrect = ai_response_json.get("correctBinType", "") == input.binTypeGuess.value
        logger.info(f"isBinTypeGuessCorrect: {isBinTypeGuessCorrect}")
        pointsEarned = 0
        if isBinTypeGuessCorrect:
            logger.info(f"Updating user score")
            pointsEarned = 10
            update_or_create_user_score(input.user_id, 10, db)
        logger.info(f"Returning Response")
        payload = VerifyPhotoPayload(
            isBinTypeGuessCorrect=isBinTypeGuessCorrect,
            pointsEarned=pointsEarned,
            correctBinType=Bin(ai_response_json.get("correctBinType", "")),
            notesFromAI=ai_response_json.get("notesFromAI", "")
        )
        return VerifyPhotoResult(payload=payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))