import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.ingest import router as ingest_router
from api.query import router as query_router
from api.logs import router as logs_router
from api.evaluation import router as evaluation_router

app = FastAPI(title="PALO RAG API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest_router)
app.include_router(query_router)
app.include_router(logs_router)
app.include_router(evaluation_router)


@app.get("/health")
def health():
    return {"status": "ok"}
