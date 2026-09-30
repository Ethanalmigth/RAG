from contextlib import asynccontextmanager

from app.core.qdrant import init_collection
from fastapi import FastAPI
from app.controller.document import router as document_router
from app.core.engine import ENGINE,Base
from app.exception.CustomException import CustomException
from app.exception.Handler import custom_exception_handler
from app.controller.ask import router as ask_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await init_collection()
    yield

app = FastAPI(lifespan=lifespan,title="My RAG Project")
app.include_router(document_router)
app.include_router(ask_router)
app.add_exception_handler(CustomException, custom_exception_handler)
@app.get("/")
def read_root():
    return {"message": "Bienvenue dans mon projet RAG avec FastAPI !"}

@app.get("/health")
def health_check():
    return {"status": "ok"}



