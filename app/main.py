from fastapi import FastAPI
from . import models
from .database import engine
from .routes import router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

print(">> Tabelas criadas!")

app = FastAPI()
app.include_router(router)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)