from fastapi import  FastAPI 
from database import create_db_tables, engine, SessionDep
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_tables(engine)
    yield






