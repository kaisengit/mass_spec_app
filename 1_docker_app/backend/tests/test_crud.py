import pytest
from mass_spec_app.api import schemas
from mass_spec_app.config import DATABASE_URL_TEST
from mass_spec_app.db.crud import (
    create_compound,
    get_measured_compounds_filtered,
)
from mass_spec_app.db.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

engine = create_engine(DATABASE_URL_TEST)
if not database_exists(engine.url):
    print("create test db")
    create_database(engine.url)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


@pytest.fixture(scope="function")
def db_session():
    # Setup the test database before each test
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_create_compound(db_session):
    """Test creating a compound entry in the database."""
    compound_create = schemas.CompoundCreate(
        compound_id=1,
        compound_name="Test Compound",
        molecular_formula="C10H8O2",  # This will be computed in CRUD
        type="chemical",
    )

    new_compound = create_compound(db_session, compound_create)

    assert new_compound.compound_name == "Test Compound"
    assert new_compound.molecular_formula == "C10H8O2"


def test_get_measured_compounds_filtered(db_session):
    """Test filtering measured compounds via CRUD function."""
    # Assume data exists in the database
    compounds = get_measured_compounds_filtered(db_session)
    assert isinstance(compounds, list)


@pytest.fixture(scope="session", autouse=True)
# remove the test db after all tests
def cleanup(request):
    def __cleanup():
        if database_exists(engine.url):
            print("remove test db")
            drop_database(engine.url)

    request.addfinalizer(__cleanup)
