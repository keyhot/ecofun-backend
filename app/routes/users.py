from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
import app.models as models
import app.schemas as schemas
from fastapi import APIRouter
from app.database import get_db

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.get('/', response_model=List[schemas.CreateUser])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.UserScore).all()
    return users

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=List[schemas.CreateUser])
def create_user(user_data: schemas.CreateUser, db: Session = Depends(get_db)):
    new_user = models.UserScore(**user_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return [new_user]

@router.get('/{id}', response_model=schemas.CreateUser, status_code=status.HTTP_200_OK)
def get_user_by_id(id: str, db: Session = Depends(get_db)):
    user = db.query(models.UserScore).filter(models.UserScore.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The id: {id} you requested for does not exist")
    return user

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: str, db: Session = Depends(get_db)):
    user_to_delete = db.query(models.UserScore).filter(models.UserScore.id == id)
    if user_to_delete.first() is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The id: {id} you requested for does not exist")
    user_to_delete.delete(synchronize_session=False)
    db.commit()

@router.put('/{id}', response_model=schemas.User)
def update_user(update_data: schemas.User, id: str, db: Session = Depends(get_db)):
    user_to_update = db.query(models.UserScore).filter(models.UserScore.id == id)
    if user_to_update.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id: {id} does not exist")
    user_to_update.update(update_data.dict(), synchronize_session=False)
    db.commit()
    return user_to_update.first()
