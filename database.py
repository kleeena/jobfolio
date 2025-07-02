from fastapi import Depends
import os
from sqlmodel import Field, SQLModel, create_engine, Session
from models import User, Resume, JobApplication
from typing import Annotated

SQLITE_FILE_NAME = 'database.db'
SQLITE_URL = f"sqlite:///{SQLITE_FILE_NAME}"

engine = create_engine(SQLITE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_tables(engine):
    try:
        if 'database.db' not in os.listdir():
            SQLModel.metadata.create_all(engine)
    except:
        raise('A problem occurred while building the database.')
    
SessionDep = Annotated[Session, Depends(get_session)]

create_db_tables(engine)