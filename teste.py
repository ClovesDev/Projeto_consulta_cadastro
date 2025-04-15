import google.generativeai as genai
import os

gemini_api_key = os.getenv("AIzaSyBI9Yx0YqvXQ7__2BO6cErnFINYfackqq8")

if not gemini_api_key:
        print("Erro: Variável de ambiente AIzaSyBI9Yx0YqvXQ7__2BO6cErnFINYfackqq8 não está configurada.")
else:
        try:
            genai.configure(api_key=gemini_api_key)
            print("Chave de API configurada com sucesso!")
            model = genai.GenerativeModel("gemini-2.0-flash") 
            response = model.generate_content("Diga Olá")
            print(response.text)
        except Exception as e:
            print(f"Erro ao testar a chave de API: {e}")