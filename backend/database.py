from pathlib import Path
from sqlmodel import create_engine, Session, SQLModel
from .models import *

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sqlite_file_name = str(PROJECT_ROOT / "toefl_simulator.db")
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=False, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
