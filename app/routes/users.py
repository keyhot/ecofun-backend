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
def test_posts(db: Session = Depends(get_db)):
    user = db.query(models.UserScore).all()
    return user

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=List[schemas.CreateUser])
def test_posts_sent(post_post:schemas.CreateUser, db:Session = Depends(get_db)):
    new_user = models.UserScore(**post_post.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return [new_user]

@router.get('/{id}', response_model=schemas.CreateUser, status_code=status.HTTP_200_OK)
def get_test_one_post(id:int ,db:Session = Depends(get_db)):
    idv_post = db.query(models.Post).filter(models.Post.id == id).first()
    if idv_post is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The id: {id} you requested for does not exist")
    return idv_post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_test_post(id:int, db:Session = Depends(get_db)):

    deleted_post = db.query(models.UserScore).filter(models.UserScore.id == id)

    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"The id: {id} you requested for does not exist")
    deleted_post.delete(synchronize_session=False)
    db.commit()

@router.put('/posts/{id}', response_model=schemas.User)
def update_test_post(update_post:schemas.User, id:int, db:Session = Depends(get_db)):

    updated_post =  db.query(models.Post).filter(models.UserScore.id == id)

    if updated_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{id} does not exist")
    updated_post.update(update_post.dict(), synchronize_session=False)
    db.commit()

    return  updated_post.first()