from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    marca: str
    modelo: str
    ano: int
    cilindrada: int
    vel_max: int
    torque: float
    usabilidade: str
    cor: str
    categoria: str
    quilometragem: str
    avaliacoes: int
    consumo: str
    imagem: str
    preco: float

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True