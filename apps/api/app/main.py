from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import errors, health, projects, review, share
from app.core.config import settings
from app.db.session import init_db


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    init_db()  # create_all untuk SQLite; ganti Alembic saat pindah PostgreSQL
    yield


app = FastAPI(title="ThesisTwin API", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware, allow_origins=settings.cors_origins, allow_methods=["*"], allow_headers=["*"]
)
errors.register(app)
app.include_router(health.router)
app.include_router(projects.router)
app.include_router(review.router)
app.include_router(share.router)
