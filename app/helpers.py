from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.orm import class_mapper
import sqlalchemy
from starlette import status
import app.models as models
import app.schemas as schemas
from app.database import get_db
import logging

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

logger = logging.getLogger(__name__)

# NOTE: Depends() doesn't work with simple functions, only with routes. So we need to use it with a route and then call the function from there

# Users
def get_users(db: Session = Depends(get_db)):
    print(db)
    users = db.query(models.UserScore).all()
    return users

def create_user(user_data: schemas.CreateUser, db: Session = Depends(get_db)):
    new_user = models.UserScore(**user_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return [new_user]

def get_user_by_id(id: int, db: Session) -> dict:
    user = db.query(models.UserScore).filter(models.UserScore.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The id: {id} you requested for does not exist")
    return user.as_dict()

def delete_user(id: int, db: Session = Depends(get_db)):
    user_to_delete = db.query(models.UserScore).filter(models.UserScore.id == id)
    if user_to_delete.first() is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The id: {id} you requested for does not exist")
    user_to_delete.delete(synchronize_session=False)
    db.commit()

def update_user(update_data: schemas.User, id: int, db: Session = Depends(get_db)):
    user_to_update = db.query(models.UserScore).filter(models.UserScore.id == id)
    if user_to_update.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id: {id} does not exist")
    user_to_update.update(update_data.dict(), synchronize_session=False)
    db.commit()
    return user_to_update.first()

def update_or_create_user_score(user_id: str, pointsEarned: int, db: Session) -> models.UserScore:
    user = db.query(models.UserScore).filter(models.UserScore.id == user_id).first()
    logger.info(f"User: {user}")
    if user:
        logger.info(f"Adding {pointsEarned} points to user {user_id}: {user.score} -> {user.score + pointsEarned}")
        user.score = user.score + pointsEarned
    else:
        logger.info(f"Creating new user {user_id} with {pointsEarned} points")
        user = models.UserScore(id=user_id, score=pointsEarned)
        db.add(user)
    
    db.commit()
    db.refresh(user)
    return user


# Marketplaces
def get_marketplaces(db: Session = Depends(get_db)) -> List[schemas.CreateMarketplace]:
    marketplaces = db.query(models.MarketplaceUnit).all()
    return marketplaces

def create_marketplace(marketplace_data: schemas.CreateMarketplace, db: Session = Depends(get_db)) -> List[schemas.CreateMarketplace]:
    new_marketplace = models.MarketplaceUnit(**marketplace_data.dict())
    db.add(new_marketplace)
    db.commit()
    db.refresh(new_marketplace)
    return [new_marketplace]

def get_marketplace_by_id(id: int, db: Session) -> dict:
    logger.info(f"Getting marketplace with id: {id}")
    marketplace = db.query(models.MarketplaceUnit).filter(models.MarketplaceUnit.id == id).first()
    if marketplace is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The id: {id} you requested for does not exist")
    logger.info(f"Returning marketplace with id: {id}")
    return marketplace.as_dict()

def delete_marketplace(id: int, db: Session = Depends(get_db)):
    marketplace_to_delete = db.query(models.MarketplaceUnit).filter(models.MarketplaceUnit.id == id)
    if marketplace_to_delete.first() is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The id: {id} you requested for does not exist")
    marketplace_to_delete.delete(synchronize_session=False)
    db.commit()

def update_marketplace(update_data: schemas.Marketplace, id: int, db: Session = Depends(get_db)) -> schemas.Marketplace:
    marketplace_to_update = db.query(models.MarketplaceUnit).filter(models.MarketplaceUnit.id == id)
    if marketplace_to_update.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id: {id} does not exist")
    marketplace_to_update.update(update_data.dict(), synchronize_session=False)
    db.commit()
    return marketplace_to_update.first()
