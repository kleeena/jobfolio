from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pydantic import EmailStr
from datetime import date


class User(SQLModel, table=True):
    id : int = Field(primary_key=True)
    first_name : str = Field(nullable=False)
    last_name : str = Field(nullable=False)
    email : EmailStr = Field(unique=True)
    password_hash: str =  Field()

