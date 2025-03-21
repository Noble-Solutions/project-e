from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.db.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)
origins = [
    "http://localhost:5173",
    "http://80.90.178.200:80",
    "https://4375901-fj52928.twc1.net:8443/",
    "https://4375901-fj52928.twc1.net",
    "http://localhost",
    "http://80.90.178.200",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "POST", "PATCH", "PUT"],
    allow_headers=["*"],
)
