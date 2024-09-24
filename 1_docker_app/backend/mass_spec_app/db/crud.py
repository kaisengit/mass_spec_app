# 2024-09 Kai-Michael Kammer
"""
Contains the core database interaction logic, providing CRUD (Create, Read, Update, Delete)
operations for compounds, measured-compounds, adducts and retention times.
Implements business logic for ensuring data integrity and querying with filtering.
"""  # noqa: E501
from typing import List, Optional

from sqlalchemy.orm import Session

from mass_spec_app.api import schemas
from mass_spec_app.db import models
from mass_spec_app.scripts.chem_utils import (
    get_measured_formula,
    get_monoisotopic_mass,
)


# Adduct CRUD
def get_adducts(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.Adduct]:
    """Retrieve a list of adducts with pagination."""
    return db.query(models.Adduct).offset(skip).limit(limit).all()


def create_adduct(db: Session, adduct: schemas.AdductCreate) -> models.Adduct:
    db_adduct = models.Adduct(
        adduct_name=adduct.adduct_name,
        mass_adjustment=adduct.mass_adjustment,
        ion_mode=adduct.ion_mode,
    )
    db.add(db_adduct)
    db.commit()
    return db_adduct


# Compound CRUD
def create_compound(
    db: Session, compound: schemas.CompoundCreate
) -> models.Compound:
    # Compute the molecular mass and formula using molmass package
    # Attempt to validate the molecular formula
    # Ensure the molecular formula has the correct isotope notation
    monoisotopic_mass = get_monoisotopic_mass(compound.molecular_formula)

    db_compound = models.Compound(
        compound_id=compound.compound_id,
        compound_name=compound.compound_name,
        molecular_formula=compound.molecular_formula,
        type=compound.type,
        computed_mass=monoisotopic_mass,  # Use the computed monoisotopic mass
    )
    db.add(db_compound)
    db.commit()
    return db_compound


def get_compounds(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.Compound]:
    """Retrieve a list of compounds with pagination."""
    return db.query(models.Compound).offset(skip).limit(limit).all()


# Retention Time CRUD (with get_or_create)
# CRUD for Retention Times
def get_retention_times(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.RetentionTime]:
    """Retrieve a list of retention times with pagination."""
    return db.query(models.RetentionTime).offset(skip).limit(limit).all()


def get_or_create_retention_time(
    db: Session, retention_time: schemas.RetentionTimeCreate
) -> models.RetentionTime:
    existing_retention_time = (
        db.query(models.RetentionTime)
        .filter_by(retention_time=retention_time.retention_time)
        .first()
    )

    if existing_retention_time:
        return existing_retention_time

    new_retention_time = models.RetentionTime(
        retention_time=retention_time.retention_time,
        comment=retention_time.comment,
    )
    db.add(new_retention_time)
    db.commit()
    return new_retention_time


# Measured Compound CRUD
def get_measured_compounds(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.MeasuredCompound]:
    """Retrieve a list of measured compounds with pagination."""
    return db.query(models.MeasuredCompound).offset(skip).limit(limit).all()


# Create Measured Compound (with adduct mapping from the database)
def create_measured_compound_and_retention_time(
    db: Session, measured_compound: schemas.MeasuredCompoundCreate
) -> models.MeasuredCompound:
    # Query the adduct_id from the adducts table using the adduct_name
    adduct = (
        db.query(models.Adduct)
        .filter(models.Adduct.adduct_name == measured_compound.adduct_name)
        .first()
    )

    if not adduct:
        raise ValueError(
            f"Adduct '{measured_compound.adduct_name}'"
            f" not found in the database."
        )

    # Fetch compound to calculate the measured mass
    compound = (
        db.query(models.Compound)
        .filter(models.Compound.compound_id == measured_compound.compound_id)
        .first()
    )

    if not compound:
        raise ValueError(
            f"Compound '{measured_compound.compound_id}'"
            f" not found in the database."
        )
        # retentiont ime
    retention_time_create = schemas.RetentionTimeCreate(
        retention_time=measured_compound.retention_time,
        comment=measured_compound.retention_time_comment,
    )
    retention_time_entry = get_or_create_retention_time(
        db, retention_time=retention_time_create
    )

    # get the adjusted molecula formula
    molecular_formula = get_measured_formula(
        compound.molecular_formula, adduct_name=adduct.adduct_name
    )
    # Calculate measured mass using the compound's mass and adduct's mass adjustment  # noqa: E501
    measured_mass = get_monoisotopic_mass(molecular_formula=molecular_formula)

    # Create the MeasuredCompound entry
    db_measured_compound = models.MeasuredCompound(
        compound_id=measured_compound.compound_id,
        adduct_id=adduct.adduct_id,
        retention_time_id=retention_time_entry.retention_time_id,
        measured_mass=measured_mass,
        molecular_formula=molecular_formula,
    )
    db.add(db_measured_compound)
    db.commit()
    return db_measured_compound


# Single GETs
# CRUD to Get a Single Adduct by ID
def get_adduct_by_id(db: Session, adduct_id: int) -> Optional[models.Adduct]:
    """Retrieve an adduct by its ID."""
    return (
        db.query(models.Adduct)
        .filter(models.Adduct.adduct_id == adduct_id)
        .first()
    )


# CRUD to Get a Single Compound by ID
def get_compound_by_id(
    db: Session, compound_id: int
) -> Optional[models.Compound]:
    """Retrieve a compound by its ID."""
    return (
        db.query(models.Compound)
        .filter(models.Compound.compound_id == compound_id)
        .first()
    )


# CRUD to Get a Single Measured Compound by ID
def get_measured_compound_by_id(
    db: Session, measured_compound_id: int
) -> Optional[models.MeasuredCompound]:
    """Retrieve a measured compound by its ID."""
    return (
        db.query(models.MeasuredCompound)
        .filter(
            models.MeasuredCompound.measured_compound_id
            == measured_compound_id
        )
        .first()
    )


# CRUD to Get a Single Retention Time by ID
def get_retention_time_by_id(
    db: Session, retention_time_id: int
) -> Optional[models.RetentionTime]:
    """Retrieve a retention time by its ID."""
    return (
        db.query(models.RetentionTime)
        .filter(models.RetentionTime.retention_time_id == retention_time_id)
        .first()
    )


# CRUD to query measured components with a filter
def get_measured_compounds_filtered(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    retention_time: float = None,
    compound_type: str = None,
    ion_mode: str = None,
) -> List[models.MeasuredCompound]:
    # Start the query on MeasuredCompound, and join related tables
    query = (
        db.query(models.MeasuredCompound)
        .join(
            models.Compound,
            models.MeasuredCompound.compound_id == models.Compound.compound_id,
        )
        .join(
            models.RetentionTime,
            models.MeasuredCompound.retention_time_id
            == models.RetentionTime.retention_time_id,
        )
        .join(
            models.Adduct,
            models.MeasuredCompound.adduct_id == models.Adduct.adduct_id,
        )
    )

    # Apply filters
    if retention_time is not None:
        if retention_time < 0:
            raise ValueError("retention_time must be positive")
        query = query.filter(
            models.RetentionTime.retention_time == retention_time
        )

    if compound_type is not None:
        query = query.filter(models.Compound.type == compound_type)

    if ion_mode is not None:
        query = query.filter(models.Adduct.ion_mode == ion_mode)

    # Return the final query result
    query = query.offset(skip).limit(limit)
    return query.all()
