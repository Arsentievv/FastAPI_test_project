from fastapi import FastAPI
from src.config import get_settings
from src.materials.router import router as material_router
from src.collections.router import router as collection_router

settings = get_settings()


app = FastAPI(title="FastAPI PyTest")

app.include_router(material_router, tags=["materials"])
app.include_router(collection_router, tags=["collections"])

