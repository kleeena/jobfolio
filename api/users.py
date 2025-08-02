from fastapi import APIRouter, HTTPException

from db.database import SessionDep, get_session
from models.models import User, JobApplication, Resume
from schemas.users import UserCreate, UserUpdate

router = APIRouter()

@router.post('/user')
def create_user(user: UserCreate, session : SessionDep) -> User:
    """
    Create a new user in the database.

    Args:
        user (UserCreate): User creation schema containing user details.
        session (SessionDep): Database session dependency.

    Returns:
        User: The created user object.
    
    """
    created_user = user.create_users_in_db(session)
    return created_user

@router.get('/user/{user_id}')
def read_user(user_id: int | None, session: SessionDep):
    """
    Retrieve a user by their ID.

    Args:
        user_id (int | None): The ID of the user to retrieve. Must not be None.
        session (SessionDep): Database session dependency.

    Raises:
        HTTPException: If user_id is None (400) or user is not found (404).

    Returns:
        User: The retrieved user object.
    """
    if user_id is not None:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
    else:
        raise HTTPException(status_code=400, detail="User ID not specified.")
    return user

@router.patch('/user/{user_id}')
def update_user(user_id:int, user_update: UserUpdate, session: SessionDep):
    """
    Update an existing user in the database.

    Args:
        user_id (int): The ID of the user to update.
        user_update (UserUpdate): User update schema with new data.
        session (SessionDep): Database session dependency.

    Raises:
        HTTPException: If the user is not found (404).

    Returns:
        User: The updated user object.
    """
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
    """
    Delete a user from the database.

    Args:
        user_id (int): The ID of the user to delete.
        session (SessionDep): Database session dependency.

    Raises:
        HTTPException: If the user is not found (404).

    Returns:
        dict: Confirmation of deletion with {"OK": True}.
    
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"OK": True}