# 2024-09 Kai-Michael Kammer
"""
Script responsible for populating the database with initial data from external input files.
It processes raw data, maps it to the relevant models, and inserts it into the database.
"""  # noqa: E501
import json
import logging
from datetime import datetime, timezone

import pandas as pd
from mass_spec_app.api import schemas
from mass_spec_app.db import crud, models
from mass_spec_app.scripts import chem_utils as cu
from sqlalchemy.orm import Session

# File paths
ADDUCTS_FILE = "./migration/adducts.json"
COMPOUNDS_FILE = "./migration/compounds.xlsx"
MEASURED_COMPOUNDS_FILE = "./migration/measured-compounds.xlsx"


# table to verify that initial migration was done
def check_initialization_status(db: Session) -> bool:
    """Check if the database has been initialized."""
    status = db.query(models.InitializationStatus).first()
    return status is not None and status.is_initialized


def set_initialization_status(db: Session) -> None:
    """Set the database as initialized with a timezone-aware timestamp."""
    status = models.InitializationStatus(
        is_initialized=True,
        initialized_at=datetime.now(
            tz=timezone.utc
        ),  # Use timezone-aware datetime
    )
    db.add(status)
    db.commit()


def populate_adducts(db: Session) -> None:
    """Populate the Adducts table using the AdductCreate schema."""
    logging.info("Populating Adducts")
    with open(ADDUCTS_FILE) as f:
        adducts_data = json.load(f)

    for adduct in adducts_data:
        # Create an AdductCreate schema object
        adduct_create = schemas.AdductCreate(
            adduct_name=adduct["name"],
            mass_adjustment=float(adduct["mass"]),
            ion_mode=adduct["ion_mode"],
        )
        # Use the CRUD function to insert into the database
        crud.create_adduct(db, adduct_create)


def populate_compounds(db: Session) -> None:
    """Populate the Compounds table from compounds.xlsx using the CompoundCreate schema."""  # noqa: E501
    logging.info("Populating Compounds")
    compounds_df = pd.read_excel(COMPOUNDS_FILE)

    for _, row in compounds_df.iterrows():
        # Handle NaN values in the 'type' column by setting a default value (like None or "Unknown")  # noqa: E501
        compound_type = (
            row["type"] if pd.notna(row["type"]) else None
        )  # Set to None if NaN, or "Unknown" as an alternative
        # we sanitize molecular formulas on import
        molecular_formula = cu.convert_isotope_notation(
            row["molecular_formula"]
        )
        # Create a CompoundCreate schema object
        compound_create = schemas.CompoundCreate(
            compound_id=row["compound_id"],
            compound_name=row["compound_name"],
            molecular_formula=molecular_formula,
            type=compound_type,
        )
        # Use the CRUD function to insert into the database
        crud.create_compound(db, compound_create)


def populate_measured_compounds(db: Session) -> None:
    """Populate the MeasuredCompounds table using the MeasuredCompoundCreate schema."""  # noqa: E501
    logging.info("Populating Measured Compounds")
    measured_compounds_df = pd.read_excel(MEASURED_COMPOUNDS_FILE)

    for _, row in measured_compounds_df.iterrows():
        # Get the adduct_name from the file (assuming the column is present)
        adduct_name = row.get("adduct_name")
        retention_time = row.get("retention_time")
        # Handle NaN values in the 'type' column by setting a default value (like None or "Unknown")  # noqa: E501
        retention_time_comment = (
            row["retention_time_comment"]
            if pd.notna(row["retention_time_comment"])
            else None
        )  # Set to None if NaN, or "Unknown" as an alternativeion_time from input  # noqa: E501

        if not adduct_name:
            print(
                f"Adduct name missing for compound {row['compound_name']}. Skipping entry."  # noqa: E501
            )
            continue

        # Prepare MeasuredCompoundCreate schema using RetentionTime model
        measured_compound_create = schemas.MeasuredCompoundCreate(
            compound_id=row["compound_id"],
            adduct_name=adduct_name,
            retention_time=retention_time,
            retention_time_comment=retention_time_comment,
        )

        try:
            # Create measured compound
            crud.create_measured_compound_and_retention_time(
                db, measured_compound_create
            )
        except ValueError as e:
            print(f"Error: {e}. Skipping entry.")


def populate_data(db: Session) -> None:
    """Populate the database only if it hasn't been initialized."""
    logging.info("Populating Initial Data")
    if not check_initialization_status(db):
        # Populate Adducts
        populate_adducts(db)

        # Populate Compounds
        populate_compounds(db)

        # Populate Measured Compounds
        populate_measured_compounds(db)

        # set DB as initialized
        set_initialization_status(db)

        print("Initial database population completed.")
    else:
        print("DB Already Populated")
