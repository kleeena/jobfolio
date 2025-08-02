from pydantic import BaseModel, EmailStr
from sqlmodel import Field

from db.database import SessionDep
from models.models import User

class UserCreate(BaseModel):
    """
    Represents the data required to create a new user.

    This class defines the attributes for a new user, including their
    first name, last name, email, and a hashed password.

    Attributes:
        first_name    : The user's first name.
        last_name     : The user's last name.
        email         : The user's email address, which must be unique.
        password_hash : The hashed password for the user.

    """
    first_name: str = Field(nullable=False)
    last_name : str = Field(nullable=False)
    email : EmailStr = Field(unique=True)
    password_hash: str =  Field(nullable=False)

    def create_users_in_db(self, session: SessionDep):
        """
        Creates a new user record in the database.

        Args:
            session: The database session dependency.

        Returns:
            The newly created User object from the database.
        
        """
        user_db = User(
        first_name=self.first_name,
        last_name=self.last_name,
        email=self.email,
        password_hash=self.password_hash)
        session.add(user_db)
        session.commit()
        session.refresh(user_db)
        return user_db
    

class UserUpdate(UserCreate):
    """
    Represents the data for updating an existing user.

    This class inherits from `UserCreate` but makes all fields optional,
    allowing for partial updates to a user's information.

    Attributes:
        first_name    : The user's new first name (optional).
        last_name     : The user's new last name (optional).
        email         : The use r's new email address (optional).
        password_hash : The user's new hashed password (optional).

    """
    first_name : str | None = None
    last_name : str | None = None
    email : EmailStr | None = None
    password_hash : str | None = None
    