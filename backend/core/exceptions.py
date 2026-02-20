from fastapi import Request
from fastapi.responses import JSONResponse


class GuardrailException(Exception):
    def __init__(self, reason: str):
        self.reason = reason


class ProviderUnavailableException(Exception):
    pass


class VectorStoreException(Exception):
    pass


async def guardrail_exception_handler(request: Request, exc: GuardrailException):
    return JSONResponse(status_code=400, content={"detail": exc.reason})


async def provider_unavailable_handler(request: Request, exc: ProviderUnavailableException):
    return JSONResponse(status_code=503, content={"detail": "AI provider unavailable"})


async def vectorstore_exception_handler(request: Request, exc: VectorStoreException):
    return JSONResponse(status_code=500, content={"detail": "Vector store error"})
