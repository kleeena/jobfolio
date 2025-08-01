from pydantic import BaseModel
from pydantic.networks import AnyUrl
from typing import Optional

from database import SessionDep
from models import Resume

class ResumeBase(BaseModel):
    id: int
    version_name : str 
    created_at : str 
    description : str 
    file_url : str 
    is_active : bool  
    target_roles : str  
    user_id : int 

class CreateResume(BaseModel):
    version_name : str 
    description : str | None
    file_url : str 
    is_active : bool 
    target_roles : str 
    user_id : int

    def create_resume_db(self, session: SessionDep):
        resume_db = Resume(
            version_name= self.version_name,
            description = self.description,
            file_url= self.file_url,
            is_active = self.is_active,
            target_roles = self.target_roles,
            user_id = self.user_id
        )
        session.add(resume_db)
        session.commit()
        session.refresh(resume_db)
        return resume_db

class UpdateResume(BaseModel):
    version_name : Optional[str]
    description : Optional[str]
    file_url : Optional[str]
    is_active: Optional[bool]
    target_roles: Optional[str]
    user_id: int

    def update_resume(self, resume_id: int, session: SessionDep):
        resume_db = session.get(Resume, resume_id)
        if not resume_db:
            raise HTTPException(status_code = 404, detail= "Resume not found")
        updated_resume_data = self.model_dump(exclude_unset=True)
        resume_db.sqlmodel_update(resume_data)
        session.add(resume_db)
        session.commit()
        session.refresh(resume_db)
        return resume_db
    





