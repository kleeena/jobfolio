from fastapi import APIRouter
from sqlmodel import select

from schemas.resume import CreateResume, UpdateResume
from db.database import SessionDep
from models.models import Resume

router = APIRouter()


@router.get('/resume/{resume_id}')
async def get_resume(resume_id:int, session: SessionDep):
    resume = session.get(Resume, resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume

@router.get('/resume', response_model = list[Resume])
async def get_resume_list(session: SessionDep):
    resumes = session.exec(select(Resume)).all()
    return resumes


@router.post('/resume')
async def create_resume(resume_data: CreateResume, session: SessionDep):
    resume_db = resume_data.create_resume_db(session)
    return resume_data

@router.patch('/resume/{resume_id}')
async def update_resume(resume_data: UpdateResume, resume_id: int, session:SessionDep):
    resume_db = resume_data.update_resume(resume_id, session)
    return resume_db

@router.delete('/resume/{resume_id}')
async def delete_resume(resume_id: int, session: SessionDep):
    resume = session.get(Resume, resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    session.delete(resume)
    session.commit()
    return {"OK": True}