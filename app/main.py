from fastapi import FastAPI
from app.interfaces.api.routes import generation, verification, setups

app = FastAPI(title="AutoAumento API")

app.include_router(generation.router, prefix="/generation", tags=["generation"])
app.include_router(verification.router, prefix="/verification", tags=["verification"])
app.include_router(setups.router, prefix="/setups", tags=["setups"])
