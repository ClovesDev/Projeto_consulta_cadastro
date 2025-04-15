from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Item(Base):
    __tablename__ = "motos"

    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String, index=True)
    modelo = Column(String)
    ano = Column(Integer)
    cilindrada = Column(Integer)
    vel_max = Column(Integer)
    torque = Column(Float)
    usabilidade = Column(String)
    cor = Column(String)
    categoria = Column(String)
    quilometragem = Column(String)
    avaliacoes = Column(Integer)
    consumo = Column(String)
    imagem = Column(String)
    preco = Column(Float)