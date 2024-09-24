import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

from mass_spec_app import config
from mass_spec_app.app import app
from mass_spec_app.db.models import Base
from mass_spec_app.db.session import get_db

# Setup test database connection
engine = create_engine(config.DATABASE_URL_TEST)
if not database_exists(engine.url):
    print("create test db")
    create_database(engine.url)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


# Dependency override
def override_get_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_get_measured_compounds():
    """Test GET /measured-compounds endpoint."""
    response = client.get("/measured-compounds")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_compound():
    """Test POST /compounds endpoint for creating a compound."""
    response = client.post(
        "/compounds/",
        json={
            "compound_id": 0,
            "compound_name": "Water",
            "molecular_formula": "H2O",
            "type": "simple",
            "computed_mass": 18.015,
        },
    )
    assert response.status_code == 200
    assert response.json()["compound_name"] == "Water"


@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    def __cleanup():
        if database_exists(engine.url):
            drop_database(engine.url)
            print("remove test db")

    request.addfinalizer(__cleanup)
