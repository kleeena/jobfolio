from fastapi import Depends
import os
from sqlmodel import Field, SQLModel, create_engine, Session
from models.models import User, Resume, JobApplication
from typing import Annotated

os.makedirs("db", exist_ok=True)

SQLITE_FILE_NAME = os.path.join("db", "database.db")
SQLITE_URL = f"sqlite:///{SQLITE_FILE_NAME}"

engine = create_engine(SQLITE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_tables(engine):
    try:
        if not os.path.exists(SQLITE_FILE_NAME):
            SQLModel.metadata.create_all(engine)
    except Exception as e:
        raise RuntimeError("A problem occurred while building the database.") from e
    
SessionDep = Annotated[Session, Depends(get_session)]

create_db_tables(engine)