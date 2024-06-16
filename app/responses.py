from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

class Bin(Enum):
    PAPER = "PAPER"
    GLASS = "GLASS"
    BIO = "BIO"
    METAL_PLASTIC = "METAL_PLASTIC"
    MIXED = "MIXED" 

class MainScreen(BaseModel):
    id: str = Field(..., example="example@gmail.com")
    marketplaces: list = Field(..., example=[{"id": 1, "image": "https://example.com/image.jpg", "title": "Title", "description": "Description", "price": 100}])
    pointsAmount: int = Field(..., example=1005)


class VerifyPhotoPayload(BaseModel):
    isBinTypeGuessCorrect: bool
    pointsEarned: int = Field(..., example=2)
    correctBinType: Bin
    notesFromAI: Optional[str] = Field(
        None,
        description="If wrong there will be an explanation why",
        example="Oh no, your guess was wrong, you should use the PAPER bin."
    )

class VerifyPhotoResult(BaseModel):
    status_code: int = Field(200, example=200)
    payload: VerifyPhotoPayload

