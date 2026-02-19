from fastapi import APIRouter
from api.v1 import query, ingest, logs, evaluation

api_router = APIRouter(prefix="/api")
api_router.include_router(query.router)
api_router.include_router(ingest.router)
api_router.include_router(logs.router)
api_router.include_router(evaluation.router)
