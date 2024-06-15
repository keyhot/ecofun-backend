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
    name: str = Field(..., example="Kasia Kasia")
    creationDate: str = Field(..., example="2016-08-29T09:12:33.001Z")
    pointsAmount: int = Field(..., example=1005)

class VerifyPhotoResult(BaseModel):
    isBinTypeGuessCorrect: bool
    pointsEarned: int = Field(..., example=2)
    correctBinType: Bin
    notesFromAI: Optional[str] = Field(
        None,
        description="If wrong there will be an explanation why",
        example="Oh no, your guess was wrong, you should use the PAPER bin."
    )
