from typing import Optional
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

class JobApplication(SQLModel, table=True):
    id : int = Field(primary_key=True)
    date_created : date = Field(nullable=False, default_factory=date.today)
    role : str = Field(nullable=False, index=True)
    company_name : str = Field(nullable=False)
    source : str = Field(nullable=False)
    applicaton_status : str = Field(nullable=False)
    interview_stage : str = Field(nullable=False)
    notes : str
    user_id : int = Field(foreign_key='user.id') 

class Resume(SQLModel, table=True):
    id : int = Field(primary_key=True)
    version_name : str = Field(nullable=False)
    created_at : date = Field(nullable=False, default_factory=date.today)
    description : str 
    file_url : str = Field(nullable=False)
    is_active : bool = Field(nullable=False)
    target_roles : str = Field(nullable=False)
    user_id : int = Field(foreign_key= 'user.id')


