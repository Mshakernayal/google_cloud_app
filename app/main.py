from fastapi import FastAPI

from app.database import Base, engine
from app.routers.base import router as base_router
from app.routers.posts import router as posts_router

app = FastAPI(title="CRUD Posts API")

Base.metadata.create_all(bind=engine)

app.include_router(base_router)
app.include_router(posts_router)
