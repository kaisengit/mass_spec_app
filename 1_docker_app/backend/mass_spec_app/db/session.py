# 2024-09 Kai-Michael Kammer
"""
Sets up the database connection using SQLAlchemy's engine and session maker.
Handles the lifecycle of database sessions for executing transactions within the API.
"""  # noqa: E501
from typing import Generator

from mass_spec_app.config import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session, declarative_base, sessionmaker

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base: DeclarativeMeta = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
