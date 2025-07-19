from fastapi import APIRouter
from schemas.resume import CreateResume
from database import SessionDep

router = APIRouter()

@router.post('/resume')
async def create_resume(resume_data: CreateResume, session: SessionDep):
    resume_db = resume_data.create_resume_db(session)
    return resume_data