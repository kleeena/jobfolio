from pydantic import BaseModel
from pydantic.networks import AnyUrl
from database import SessionDep
from models import Resume

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
            target_roles= self.target_roles
        )
        session.add(resume_db)
        session.commit()
        session.refresh(resume_db)
        return resume_db