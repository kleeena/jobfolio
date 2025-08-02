from fastapi import APIRouter
from sqlmodel import select

from schemas.resume import CreateResume, UpdateResume
from db.database import SessionDep
from models.models import Resume

router = APIRouter()


@router.get('/resume/{resume_id}')
async def get_resume(resume_id:int, session: SessionDep):
    """
    Retrieve a resume by its ID.

    Args:
        resume_id (int): The ID of the resume to retrieve.
        session (SessionDep): Database session dependency.

    Raises:
        HTTPException: If the resume is not found (404).

    Returns:
        Resume: The retrieved resume object.
    
    """
    resume = session.get(Resume, resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume

@router.get('/resume', response_model = list[Resume])
async def get_resume_list(session: SessionDep):
    """
    Retrieve a list of all resumes.

    Args:
        session (SessionDep): Database session dependency.

    Returns:
        list[Resume]: List of all resumes in the database.
    
    """
    resumes = session.exec(select(Resume)).all()
    return resumes


@router.post('/resume')
async def create_resume(resume_data: CreateResume, session: SessionDep):
    """
    Create a new resume in the database.

    Args:
        resume_data (CreateResume): Resume creation schema with details.
        session (SessionDep): Database session dependency.

    Returns:
        Resume: The created resume object.
    
    """
    resume_db = resume_data.create_resume_db(session)
    return resume_data

@router.patch('/resume/{resume_id}')
async def update_resume(resume_data: UpdateResume, resume_id: int, session:SessionDep):
    """
    Update an existing resume.

    Args:
        resume_data (UpdateResume): Resume update schema with new data.
        resume_id (int): The ID of the resume to update.
        session (SessionDep): Database session dependency.

    Returns:
        Resume: The updated resume object.
    
    """
    resume_db = resume_data.update_resume(resume_id, session)
    return resume_db

@router.delete('/resume/{resume_id}')
async def delete_resume(resume_id: int, session: SessionDep):
    """
    Delete a resume from the database.

    Args:
        resume_id (int): The ID of the resume to delete.
        session (SessionDep): Database session dependency.

    Raises:
        HTTPException: If the resume is not found (404).

    Returns:
        dict: Confirmation of deletion with {"OK": True}.
    
    """
    resume = session.get(Resume, resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    session.delete(resume)
    session.commit()
    return {"OK": True}