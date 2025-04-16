from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from app import models, schemas
from app.database import SessionLocal
from typing import List
from .gemini import obter_ids_e_usabilidade_gemini

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def obter_ids_e_usabilidade_db(db: Session):
    """Retorna uma lista de dicionários com ID e usabilidade de todas as motos."""
    result = db.execute(select(models.Item.id, models.Item.usabilidade))
    motos_data = [{"id": row.id, "usabilidade": row.usabilidade} for row in result]
    return motos_data

async def obter_motos_por_ids(db: Session, moto_ids: List[int]):
    """Consulta o banco de dados e retorna os detalhes das motos com os IDs fornecidos."""
    result = db.execute(select(models.Item).where(models.Item.id.in_(moto_ids)))
    motos = result.scalars().all()
    return motos

@router.get("/api/recomendar_motos")
async def recomendar_motos(uso: str = Query(..., title="Usabilidade desejada"), db: Session = Depends(get_db)):
    """Endpoint para recomendar motos com base na usabilidade, retornando detalhes completos."""
    motos_data = await obter_ids_e_usabilidade_db(db)
    if not motos_data:
        return []

    ids_recomendados = await obter_ids_e_usabilidade_gemini(motos_data, uso)
    if not ids_recomendados:
        return []

    motos_recomendadas = await obter_motos_por_ids(db, ids_recomendados)
    return motos_recomendadas

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

@router.get("/api/recomendar_ids_simples")
async def recomendar_ids(uso: str = Query(..., title="Usabilidade desejada"), db: Session = Depends(get_db)):
    """Endpoint para recomendar IDs de motos com base na usabilidade."""
    motos_data = await obter_ids_e_usabilidade_db(db)
    if not motos_data:
        return {"ids_compativeis": []}

    ids_recomendados = await obter_ids_e_usabilidade_gemini(motos_data, uso)
    return {"ids_compativeis": ids_recomendados}

@router.get("/api/motos/{item_id}", response_model=schemas.Item)
def obter_moto_por_id(item_id: int, db: Session = Depends(get_db)):
    """Endpoint para obter todos os detalhes de uma moto pelo ID."""
    moto = db.query(models.Item).filter(models.Item.id == item_id).first()
    if moto:
        return moto
    raise HTTPException(status_code=404, detail="Moto não encontrada")