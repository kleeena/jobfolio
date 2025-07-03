from pydantic import BaseModel, EmailStr
from sqlmodel import Field
from database import SessionDep
from models import User

class UserCreate(BaseModel):
    first_name: str = Field(nullable=False)
    last_name : str = Field(nullable=False)
    email : EmailStr = Field(unique=True)
    password_hash: str =  Field(nullable=False)

    def create_users_in_db(self, session: SessionDep):
        user_db = User(
        first_name=self.first_name,
        last_name=self.last_name,
        email=self.email,
        password_hash=self.password_hash)
        session.add(user_db)
        session.commit()
        session.refresh(user_db)
        return user_db



