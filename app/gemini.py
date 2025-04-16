import google.generativeai as genai
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = "AIzaSyBI9Yx0YqvXQ7__2BO6cErnFINYfackqq8"  

def configurar_api_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "Chave de API não encontrada. Por favor, configure a variável de ambiente GEMINI_API_KEY."
        )
    genai.configure(api_key=api_key)

configurar_api_gemini()
model = genai.GenerativeModel("gemini-2.0-flash")

async def obter_ids_e_usabilidade_gemini(motos_data: List[dict], uso_usuario: str):
    """Envia os IDs e usabilidade das motos para o Gemini e retorna os IDs recomendados."""
    motos_info_str = "\n".join(f"ID: {moto['id']}, Usabilidade: {moto['usabilidade']}" for moto in motos_data)

    prompt = f"""Com base na seguinte necessidade de usabilidade: "{uso_usuario}",
    e considerando as seguintes motos com seus respectivos IDs e usabilidades:

    {motos_info_str}

    Retorne apenas os IDs das motos que melhor correspondem à necessidade de usabilidade do usuário, separados por vírgula."""

    print(f"Prompt enviado para o Gemini (IDs): {prompt}")
    response = model.generate_content(prompt)
    print(f"Resposta da API do Gemini (IDs): {response.text}")

    if response and hasattr(response, "text"):
        ids_str = response.text.replace(" ", "").split(',')
        ids_recomendados = [int(id_str) for id_str in ids_str if id_str.isdigit()]
        return ids_recomendados
    return []