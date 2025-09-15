import pytest
from sqlmodel import SQLModel, create_engine, Session
from fastapi.testclient import TestClient
from pathlib import Path
from app.main import app
from app.db import get_session
from app.models import Task

@pytest.fixture(autouse=True)
def temp_db(tmp_path):
    db_file = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{db_file}", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)

    def get_test_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def client():
    return TestClient(app)
