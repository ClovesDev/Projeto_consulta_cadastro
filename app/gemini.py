import google.generativeai as genai
from app.models import Item
from sqlalchemy.orm import Session
from sqlalchemy import text

genai.configure(api_key="AIzaSyBI9Yx0YqvXQ7__2BO6cErnFINYfackqq8")

model = genai.GenerativeModel("gemini-2.0-flash")

async def recomendar_motos_gemini(uso: str, db: Session):
    prompt = f"""
    Considere uma tabela de motos com colunas: marca, modelo, ano, cilindrada, vel_max, torque, usabilidade, cor, categoria, quilometragem, avaliacoes, consumo, imagem, preco.

    Crie apenas a cláusula WHERE de uma consulta SQL que seleciona motos com base no uso: "{uso}". Não inclua SELECT, apenas a parte do filtro (ex: WHERE usabilidade ILIKE '%urbano%').

    Use ILIKE com % para permitir buscas parciais, use >= e <= para colunas de valores numericos, caso necessario filtrar por varias colunas use SEMPRE "OR" entre as clausulas (ex: WHERE usabilidade ILIKE '%urbano%' OR preco <= 20000).
    Apenas a cláusula WHERE como resposta e monte de acordo com o uso pedido usando sempre or entre as clausulas caso haja mais de uma clausula.
    """

    response = model.generate_content(prompt)
    where_clause = response.text.strip()

    if not where_clause.lower().startswith("where "):
        raise ValueError("Resposta do Gemini inválida")
    print(where_clause)

    sql = text(f"SELECT * FROM motos {where_clause}")
    print(sql)
    result = db.execute(sql)
    rows = result.fetchall()

    motos = [dict(row._mapping) for row in rows]
    return motos