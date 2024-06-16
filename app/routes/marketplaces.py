from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
import app.models as models
import app.schemas as schemas
from fastapi import APIRouter
from app.database import get_db

router = APIRouter(
    prefix='/marketplaces',
    tags=['Marketplaces']
)

@router.get('/', response_model=List[schemas.CreateMarketplace])
def get_marketplaces(db: Session = Depends(get_db)):
    marketplaces = db.query(models.MarketplaceUnit).all()
    return marketplaces

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=List[schemas.CreateMarketplace])
def create_marketplace(marketplace_data: schemas.CreateMarketplace, db: Session = Depends(get_db)):
    new_marketplace = models.MarketplaceUnit(**marketplace_data.dict())
    db.add(new_marketplace)
    db.commit()
    db.refresh(new_marketplace)
    return [new_marketplace]

@router.get('/{id}', response_model=schemas.CreateMarketplace, status_code=status.HTTP_200_OK)
def get_marketplace_by_id(id: int, db: Session = Depends(get_db)):
    marketplace = db.query(models.MarketplaceUnit).filter(models.MarketplaceUnit.id == id).first()
    if marketplace is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The id: {id} you requested for does not exist")
    return marketplace

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_marketplace(id: int, db: Session = Depends(get_db)):
    marketplace_to_delete = db.query(models.MarketplaceUnit).filter(models.MarketplaceUnit.id == id)
    if marketplace_to_delete.first() is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The id: {id} you requested for does not exist")
    marketplace_to_delete.delete(synchronize_session=False)
    db.commit()

@router.put('/{id}', response_model=schemas.Marketplace)
def update_marketplace(update_data: schemas.Marketplace, id: int, db: Session = Depends(get_db)):
    marketplace_to_update = db.query(models.MarketplaceUnit).filter(models.MarketplaceUnit.id == id)
    if marketplace_to_update.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id: {id} does not exist")
    marketplace_to_update.update(update_data.dict(), synchronize_session=False)
    db.commit()
    return marketplace_to_update.first()
