from sqlmodel import Field, SQLModel, create_engine
from models import User, Resume, JobApplication

SQLITE_FILE_NAME = 'database.db'
SQLITE_URL = f"sqlite:///{SQLITE_FILE_NAME}"

engine = create_engine(SQLITE_URL, echo=True)
SQLModel.metadata.create_all(engine)

