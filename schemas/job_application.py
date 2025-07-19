from pydantic import BaseModel
from typing import Optional, Literal
from models import JobApplication
from database import SessionDep

class CreateJobApp(BaseModel):
    role: str
    company_name : str
    source : Literal['LinkedIn', 'Company Website', 'Others']
    application_status: str
    interview_stage : str
    notes : str
    user_id : int

    def create_job_app_db(self, session: SessionDep):
        job_app_db = JobApplication(
            role= self.role,
            company_name= self.company_name,
            source= self.source,
            applicaton_status= self.application_status,
            interview_stage= self.interview_stage,
            notes= self.notes,
            user_id= self.user_id
        )
        session.add(job_app_db)
        session.commit()
        session.refresh(job_app_db)
        return job_app_db