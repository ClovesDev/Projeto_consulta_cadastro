from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal
from typing import List
from .gemini import recomendar_motos_gemini

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/motos/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/motos/", response_model=list[schemas.Item])
def read_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()

@router.get("/motos/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends (get_db)):
    db_item = db.query(models.Item). filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.put("/motos/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    for key, value in item.dict(exclude_unset=True).items():
        setattr(db_item, key, value)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/motos/{item_id}", response_model=schemas.Item)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return db_item

@router.get("/recomendar_gemini/")
async def recomendar(uso: str, db: Session = Depends(get_db)):
    try:
        return await recomendar_motos_gemini(uso, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))