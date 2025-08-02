from pydantic import BaseModel
from typing import Optional, Literal

from models.models import JobApplication
from db.database import SessionDep

class CreateJobApp(BaseModel):
    """
    Represents the data required to create a new job application.

    This class defines the attributes for a new job application, including
    details about the role, company, source, and current status.

    Attributes:
        role: The job role applied for.
        company_name: The name of the company.
        source: The platform where the application was found.
        application_status: The current status of the application.
        interview_stage: The current stage of the interview process.
        notes: Any additional notes about the application.
        user_id: The ID of the user who created this application.
    
    """
    role: str
    company_name : str
    source : Literal['LinkedIn', 'Company Website', 'Others']
    application_status: str
    interview_stage : str
    notes : str
    user_id : int

    def create_job_app_db(self, session: SessionDep):
        """
        Creates a new job application record in the database.

        Args:
            session: The database session dependency.

        Returns:
            The newly created JobApplication object from the database.
        
        """
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
    """
    Represents the data for updating an existing job application.

    This class makes all fields optional, allowing for partial updates
    to a job application record.

    Attributes:
        role: The new job role (optional).
        company_name: The new company name (optional).
        source: The new application source (optional).
        application_status: The new application status (optional).
        interview_stage: The new interview stage (optional).
        notes: The new notes for the application (optional).
        user_id: The ID of the user who owns this application.
                 This is required to ensure the correct user's application is updated.
    
    """
    role: Optional[str]
    company_name : Optional[str]
    source : Optional[Literal['LinkedIn', 'Company Website', 'Others']]
    application_status: Optional[str]
    interview_stage : Optional[str]
    notes : Optional[str]
    user_id : int

    def update_job_app(self, job_app_id: int, session: SessionDep):
        """
        Updates an existing job application record in the database.

        Args:
            job_app_id: The ID of the job application to update.
            session: The database session dependency.

        Returns:
            The updated JobApplication object from the database.

        Raises:
            HTTPException: If the job application with the given ID is not found.
        
        """
        job_app_db = session.get(JobApplication, job_app_id)
        if not job_app_db:
            raise HTTPException(status_code=404, detail='Application not found.')
        updated_job_app_data = self.model_dump(exclude_unset=True)
        job_app_db.sqlmodel_update(updated_job_app_data)
        session.add(job_app_db)
        session.commit()
        session.refresh(job_app_db)
        return job_app_db
