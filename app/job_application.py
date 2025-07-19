from database import SessionDep, get_session
from models import JobApplication
from schemas.job_application import CreateJobApp
from fastapi import APIRouter, HTTPException
from sqlalchemy import select

router = APIRouter()

@router.post('/application')
async def create_job_app(job_app: CreateJobApp, session: SessionDep):
    created_job_app = job_app.create_job_app_db(session)
    return created_job_app

@router.get('/application/{job_app_id}')
async def get_job_app(job_app_id:int, session: SessionDep):
    job_app = session.get(JobApplication, job_app_id)
    return job_app

@router.get('/applications/{user_id}')
async def get_job_app_list(user_id: int, session: SessionDep):
    stmt = select(JobApplication).where(JobApplication.user_id == user_id)
    app_list = session.scalars(statement=stmt)
    temp = []
    for application in app_list:
        app_data = application.model_dump()
        temp.append(app_data)
    return temp

    


