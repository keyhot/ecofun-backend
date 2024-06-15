import httpx
from fastapi import FastAPI, File, UploadFile, Query, Depends
from fastapi.exceptions import HTTPException
from PIL import Image
from .constants import API_KEY
from .schemas import VerifyPhoto
from .responses import MainScreen, VerifyPhotoResult
from .database import *
from .routes import users
import app.models as models
from sqlalchemy.orm import Session
import base64

app = FastAPI(tags=['EcoFun Main API'])

models.Base.metadata.create_all(bind=engine)
app.include_router(users.router)

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
async def verifyPhoto(params: VerifyPhoto, photo: UploadFile = File(...)):
    """
    Veryfies if photo and the selected bin are matching
    """
    if not photo.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only images are supported")
    photo = Image.open(photo.file)
    photo.show()
    return VerifyPhotoResult(True, 2, "PAPER", "Oh no, your guess was wrong, you should use the PAPER bin.")
