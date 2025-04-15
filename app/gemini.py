import google.generativeai as genai
from fastapi.responses import JSONResponse
from fastapi import Query
import json
import os

GEMINI_API_KEY = "AIzaSyBI9Yx0YqvXQ7__2BO6cErnFINYfackqq8"  


def configurar_api_gemini():
 
    api_key = os.getenv(GEMINI_API_KEY) 
    if not api_key:
        raise EnvironmentError(
            f"Chave de API não encontrada. Por favor, configure a variável de ambiente {GEMINI_API_KEY}."  
        )
   
genai.configure(api_key=os.getenv("AIzaSyBI9Yx0YqvXQ7__2BO6cErnFINYfackqq8"))


model = genai.GenerativeModel("gemini-2.0-flash")

async def recomendar_motos_gemini(uso: str):
    try:
        prompt = f"Recomende algumas motos boas para o uso: {uso}. Forneça tres motos que sejam compativeis com a pesquisa do usuario separados por virgula."
        print(f"Prompt enviado para o Gemini: {prompt}")

        response = model.generate_content(prompt)
        print(f"Resposta da API do Gemini: {response}") 

        if response and hasattr(response, "text"):
            recomendacoes = response.text.split('\n')
        else:
            recomendacoes = ["Erro: Resposta da API inválida"]

        return JSONResponse(content={"recomendacoes": recomendacoes})
    except Exception as e:
        print(f"Erro ao chamar a API do Gemini: {e}")