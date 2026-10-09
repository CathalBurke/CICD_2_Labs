import pytest
from fastapi.testclient import TestClient
from app.database import get_db
from app.main import app
from app.models import Base
from sqlalchemy import create_engine
from sqlalchemy .orm import Session, sessionmaker

TEST_DATABASE_URL = "sqlite+pysqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    expire_on_commit=False,
)

def overide_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = overide_get_db

@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)
    

@pytest.fixture
def client():
    return TestClient(app)