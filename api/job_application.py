from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from db.database import SessionDep, get_session
from models.models import JobApplication
from schemas.job_application import CreateJobApp, UpdateJobApp


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

@router.patch('/application/{job_app_id}')
async def update_job_app(job_app_id: int, job_app_data: UpdateJobApp, session: SessionDep):
    updated_job_app_data = job_app_data.update_job_app(job_app_id, session)
    return updated_job_app_data

@router.delete('/application/{job_app_id}')
async def delete_job_app(job_app_id: int, session:SessionDep):
    job_app_db = session.get(JobApplication, job_app_id)
    if not job_app_db:
        raise HTTPException(status_code=404, detail="Application not found")
    session.delete(job_app_db)
    session.commit()
    return {"OK": True}
    


