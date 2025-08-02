from pydantic import BaseModel
from typing import Optional, Literal

from models.models import JobApplication
from db.database import SessionDep

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

class UpdateJobApp(BaseModel):
    role: Optional[str]
    company_name : Optional[str]
    source : Optional[Literal['LinkedIn', 'Company Website', 'Others']]
    application_status: Optional[str]
    interview_stage : Optional[str]
    notes : Optional[str]
    user_id : int

    def update_job_app(self, job_app_id: int, session: SessionDep):
        job_app_db = session.get(JobApplication, job_app_id)
        if not job_app_db:
            raise HTTPException(status_code=404, detail='Application not found.')
        updated_job_app_data = self.model_dump(exclude_unset=True)
        job_app_db.sqlmodel_update(updated_job_app_data)
        session.add(job_app_db)
        session.commit()
        session.refresh(job_app_db)
        return job_app_db
