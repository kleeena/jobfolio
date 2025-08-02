from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from db.database import SessionDep, get_session
from models.models import JobApplication
from schemas.job_application import CreateJobApp, UpdateJobApp


router = APIRouter()

@router.post('/application')
async def create_job_app(job_app: CreateJobApp, session: SessionDep):
    """
    Create a new job application.

    Args:
        job_app (CreateJobApp): Job application creation schema with details.
        session (SessionDep): Database session dependency.

    Returns:
        JobApplication: The created job application object.
    
    """
    created_job_app = job_app.create_job_app_db(session)
    return created_job_app

@router.get('/application/{job_app_id}')
async def get_job_app(job_app_id:int, session: SessionDep):
    """
    Retrieve a job application by its ID.

    Args:
        job_app_id (int): The ID of the job application to retrieve.
        session (SessionDep): Database session dependency.

    Returns:
        JobApplication | None: The retrieved job application object, or None if not found.
    
    """
    job_app = session.get(JobApplication, job_app_id)
    return job_app

@router.get('/applications/{user_id}')
async def get_job_app_list(user_id: int, session: SessionDep):
    """
    Retrieve all job applications for a specific user.

    Args:
        user_id (int): The ID of the user whose applications are to be retrieved.
        session (SessionDep): Database session dependency.

    Returns:
        list[dict]: A list of job applications in dictionary form.
    
    """
    stmt = select(JobApplication).where(JobApplication.user_id == user_id)
    app_list = session.scalars(statement=stmt)
    temp = []
    for application in app_list:
        app_data = application.model_dump()
        temp.append(app_data)
    return temp

@router.patch('/application/{job_app_id}')
async def update_job_app(job_app_id: int, job_app_data: UpdateJobApp, session: SessionDep):
    """
    Update an existing job application.

    Args:
        job_app_id (int): The ID of the job application to update.
        job_app_data (UpdateJobApp): Job application update schema with new data.
        session (SessionDep): Database session dependency.

    Returns:
        JobApplication: The updated job application object.
    
    """
    updated_job_app_data = job_app_data.update_job_app(job_app_id, session)
    return updated_job_app_data

@router.delete('/application/{job_app_id}')
async def delete_job_app(job_app_id: int, session:SessionDep):
    """
    Delete a job application from the database.

    Args:
        job_app_id (int): The ID of the job application to delete.
        session (SessionDep): Database session dependency.

    Raises:
        HTTPException: If the job application is not found (404).

    Returns:
        dict: Confirmation of deletion with {"OK": True}.
    
    """
    job_app_db = session.get(JobApplication, job_app_id)
    if not job_app_db:
        raise HTTPException(status_code=404, detail="Application not found")
    session.delete(job_app_db)
    session.commit()
    return {"OK": True}
    


