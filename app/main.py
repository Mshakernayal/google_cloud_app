import time

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routers.base import router as base_router
from app.routers.posts import router as posts_router


app = FastAPI(title="CRUD Posts API")

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.on_event("startup")
def on_startup():

    max_retries = 3
    for attempt in range(max_retries):
        try:
            Base.metadata.create_all(bind=engine)
            return
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)


app.include_router(base_router)
app.include_router(posts_router)
