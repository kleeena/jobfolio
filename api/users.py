from fastapi import APIRouter, HTTPException

from db.database import SessionDep, get_session
from models import User, JobApplication, Resume
from schemas.users import UserCreate, UserUpdate

router = APIRouter()

@router.post('/user')
def create_user(user: UserCreate, session : SessionDep) -> User:
    created_user = user.create_users_in_db(session)
    return created_user

@router.get('/user/{user_id}')
def read_user(user_id: int | None, session: SessionDep):
    if user_id is not None:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
    else:
        raise HTTPException(status_code=400, detail="User ID not specified.")
    return user

@router.patch('/user/{user_id}')
def update_user(user_id:int, user_update: UserUpdate, session: SessionDep):
    user_db = session.get(User, user_id)
    if not user_id:
        raise HTTPException(status_code=404, detail='User not found!')
    user_data = user_update.model_dump(exclude_unset = True)
    user_db.sqlmodel_update(user_data)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db


@router.delete("/user/{user_id}")
def delete_hero(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"OK": True}