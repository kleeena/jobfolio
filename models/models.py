from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pydantic import EmailStr
from datetime import date


class User(SQLModel, table=True):
    """
    Represents a user in the system.

    This class defines the database model for a user, including personal
    information and authentication details.

    Attributes:
        id: The unique integer primary key for the user.
        first_name: The user's first name.
        last_name: The user's last name.
        email: The user's email address, which is unique.
        password_hash: The hashed password for the user.
    
    """
    id : int = Field(primary_key=True)
    first_name : str = Field(nullable=False)
    last_name : str = Field(nullable=False)
    email : EmailStr = Field(unique=True)
    password_hash: str =  Field()

class JobApplication(SQLModel, table=True):
    """
    Represents a job application submitted by a user.

    This class defines the database model for a job application, tracking
    its status, details, and associated user.

    Attributes:
        id: The unique integer primary key for the job application.
        date_created: The date the application was created, defaults to today.
        role: The job role applied for.
        company_name: The name of the company.
        source: The platform where the application was found.
        applicaton_status: The current status of the application.
        interview_stage: The current stage of the interview process.
        notes: Any additional notes about the application.
        user_id: The foreign key linking this application to a user.

    """
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
    """
    Represents a resume uploaded by a user.

    This class defines the database model for a user's resume, including
    versioning and other relevant metadata.

    Attributes:
        id: The unique integer primary key for the resume.
        version_name: The name or version of the resume file.
        created_at: The date the resume was created, defaults to today.
        description: A brief description of the resume.
        file_url: The URL to the hosted resume file.
        is_active: A boolean indicating if this is the user's active resume.
        target_roles: A string of comma-separated roles the resume targets.
        user_id: The foreign key linking this resume to a user.
    
    """
    id : int = Field(primary_key=True)
    version_name : str = Field(nullable=False)
    created_at : date = Field(nullable=False, default_factory=date.today)
    description : str 
    file_url : str = Field(nullable=False)
    is_active : bool = Field(nullable=False)
    target_roles : str = Field(nullable=False)
    user_id : int = Field(foreign_key= 'user.id')


