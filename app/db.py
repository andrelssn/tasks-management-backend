from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "data"
DB_PATH.mkdir(exist_ok=True)
DATABASE_URL = f"sqlite:///{DB_PATH / 'tasks.db'}"

engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
