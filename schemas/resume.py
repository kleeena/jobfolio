from pydantic import BaseModel
from pydantic.networks import AnyUrl
from typing import Optional

from db.database import SessionDep
from models.models import Resume

class ResumeBase(BaseModel):
    """
    Represents the base schema for a resume.

    This class defines the core attributes of a resume entry, typically used
    for data retrieval and display.

    Attributes:
        id: The unique identifier for the resume.
        version_name: The name or version of the resume file.
        created_at: The timestamp of when the resume was created.
        description: A brief description of the resume.
        file_url: The URL to the hosted resume file.
        is_active: A boolean indicating if this is the user's active resume.
        target_roles: A string of comma-separated roles the resume targets.
        user_id: The ID of the user who owns this resume.
    
    """
    id: int
    version_name : str 
    created_at : str 
    description : str 
    file_url : str 
    is_active : bool  
    target_roles : str  
    user_id : int 

class CreateResume(BaseModel):
    """
    Represents the data required to create a new resume.

    This class is used for validating and handling the data submitted
    when a user wants to upload a new resume.

    Attributes:
        version_name: The name or version of the resume file.
        description: A brief description of the resume (optional).
        file_url: The URL to the hosted resume file.
        is_active: A boolean indicating if this is the user's active resume.
        target_roles: A string of comma-separated roles the resume targets.
        user_id: The ID of the user who owns this resume.
    
    """
    version_name : str 
    description : str | None
    file_url : str 
    is_active : bool 
    target_roles : str 
    user_id : int

    def create_resume_db(self, session: SessionDep):
        """
        Creates a new resume record in the database.

        Args:
            session: The database session dependency.

        Returns:
            The newly created Resume object from the database.
        
        """
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
    """
    Represents the data for updating an existing resume.

    This class makes all fields optional, allowing for partial updates
    to a resume record.

    Attributes:
        version_name: The new name or version of the resume file (optional).
        description: The new description for the resume (optional).
        file_url: The new URL to the resume file (optional).
        is_active: The new active status of the resume (optional).
        target_roles: The new target roles for the resume (optional).
        user_id: The ID of the user who owns this resume. This is required
                 to ensure the correct user's resume is updated.
    
    """
    version_name : Optional[str]
    description : Optional[str]
    file_url : Optional[str]
    is_active: Optional[bool]
    target_roles: Optional[str]
    user_id: int

    def update_resume(self, resume_id: int, session: SessionDep):
        """
        Updates an existing resume record in the database.

        Args:
            resume_id: The ID of the resume to update.
            session: The database session dependency.

        Returns:
            The updated Resume object from the database.

        Raises:
            HTTPException: If the resume with the given ID is not found.
        
        """
        resume_db = session.get(Resume, resume_id)
        if not resume_db:
            raise HTTPException(status_code = 404, detail= "Resume not found")
        updated_resume_data = self.model_dump(exclude_unset=True)
        resume_db.sqlmodel_update(updated_resume_data)
        session.add(resume_db)
        session.commit()
        session.refresh(resume_db)
        return resume_db
    





