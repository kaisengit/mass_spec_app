# 2024-09 Kai-Michael Kammer
"""
Defines the API routes for all API requests to the appropriate endpoints for database interactions.
"""  # noqa: E501
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.requests import Request

import mass_spec_app.scripts.chem_utils as cu
from mass_spec_app import config
from mass_spec_app.api import schemas
from mass_spec_app.db import crud, models
from mass_spec_app.db.session import get_db

# Create an APIRouter instance
router = APIRouter()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request) -> HTMLResponse:
    """
    Serve the homepage with a link to Swagger UI.
    """
    return templates.TemplateResponse("index.html", {"request": request})


# Route for Compounds
@router.get(
    "/compounds/",
    response_model=List[schemas.Compound],
    tags=[config.STR_COMPOUNDS],
)
def read_compounds(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[models.Compound]:
    return crud.get_compounds(db, skip=skip, limit=limit)


# Route for creating Compounds
@router.post(
    "/compounds/", response_model=schemas.Compound, tags=[config.STR_COMPOUNDS]
)
def create_compound(
    compound: schemas.CompoundCreate, db: Session = Depends(get_db)
) -> models.Compound:
    try:
        return crud.create_compound(db, compound=compound)
    except ValueError as e:
        raise HTTPException(
            status_code=404, detail=f"Not able to create compound: {e}"
        )


# Route for a Single Compound by ID
@router.get(
    "/compounds/{compound_id}",
    response_model=schemas.Compound,
    tags=[config.STR_COMPOUNDS],
)
def get_compound_by_id(
    compound_id: int, db: Session = Depends(get_db)
) -> models.Compound:
    """Fetch a single compound by ID."""
    compound = crud.get_compound_by_id(db, compound_id=compound_id)
    if compound is None:
        raise HTTPException(status_code=404, detail="Compound not found")
    return compound


# Route for Adducts
@router.get(
    "/adducts/", response_model=List[schemas.Adduct], tags=[config.STR_ADDUCTS]
)
def get_adducts(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[models.Adduct]:
    """Fetch adducts with pagination."""
    return crud.get_adducts(db, skip=skip, limit=limit)


# Route for creating Adducts
@router.post(
    "/adducts/", response_model=schemas.Compound, tags=[config.STR_ADDUCTS]
)
def create_adducts(
    adduct: schemas.AdductCreate, db: Session = Depends(get_db)
) -> models.Adduct:
    return crud.create_adduct(db, adduct=adduct)


# Route for a Single Adduct by ID
@router.get(
    "/adducts/{adduct_id}",
    response_model=schemas.Adduct,
    tags=[config.STR_ADDUCTS],
)
def get_adduct_by_id(
    adduct_id: int, db: Session = Depends(get_db)
) -> models.Adduct:
    """Fetch a single adduct by ID."""
    adduct = crud.get_adduct_by_id(db, adduct_id=adduct_id)
    if adduct is None:
        raise HTTPException(status_code=404, detail="Adduct not found")
    return adduct


# Route for Measured Compounds
@router.get(
    "/measured-compounds/",
    response_model=List[schemas.MeasuredCompound],
    tags=[config.STR_MEASURED_COMPOUNDS],
)
def read_measured_compounds(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[models.MeasuredCompound]:
    return crud.get_measured_compounds(db, skip=skip, limit=limit)


# Route for Measured Compounds with filter
@router.get(
    "/measured-compounds_filtered/",
    response_model=List[schemas.MeasuredCompound],
    tags=[config.STR_MEASURED_COMPOUNDS],
)
def read_measured_compounds_filtered(
    skip: int = 0,
    limit: int = 100,
    retention_time: float = None,
    compound_type: str = None,
    ion_mode: str = None,
    db: Session = Depends(get_db),
) -> List[models.MeasuredCompound]:
    compounds = crud.get_measured_compounds_filtered(
        db,
        skip=skip,
        limit=limit,
        retention_time=retention_time,
        compound_type=compound_type,
        ion_mode=ion_mode,
    )
    if not compounds:
        raise HTTPException(
            status_code=404,
            detail="No measured compounds found with the given criteria",
        )
    return compounds


# Route for creating measured compounds
@router.post(
    "/measured-compounds/",
    response_model=schemas.MeasuredCompound,
    tags=[config.STR_MEASURED_COMPOUNDS],
)
def create_measured_compound(
    measured_compound: schemas.MeasuredCompoundCreate,
    db: Session = Depends(get_db),
) -> models.MeasuredCompound:
    try:
        return crud.create_measured_compound_and_retention_time(
            db, measured_compound=measured_compound
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404, detail=f"Not able to create compound: {e}"
        )


# Route for a Single Measured Compound by ID
@router.get(
    "/measured-compounds/{measured_compound_id}",
    response_model=schemas.MeasuredCompound,
    tags=[config.STR_MEASURED_COMPOUNDS],
)
def get_measured_compound_by_id(
    measured_compound_id: int, db: Session = Depends(get_db)
) -> models.MeasuredCompound:
    """Fetch a single measured compound by ID."""
    measured_compound = crud.get_measured_compound_by_id(
        db, measured_compound_id=measured_compound_id
    )
    if measured_compound is None:
        raise HTTPException(
            status_code=404, detail="Measured compound not found"
        )
    return measured_compound


# Route for Retention Times
@router.get(
    "/retention-times/",
    response_model=List[schemas.RetentionTime],
    tags=[config.STR_RETENTION_TIME],
)
def get_retention_times(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[models.RetentionTime]:
    """Fetch retention times with pagination."""
    return crud.get_retention_times(db, skip=skip, limit=limit)


# Route for a Single Retention Time by ID
@router.get(
    "/retention-times/{retention_time_id}",
    response_model=schemas.RetentionTime,
    tags=[config.STR_RETENTION_TIME],
)
def get_retention_time_by_id(
    retention_time_id: int, db: Session = Depends(get_db)
) -> models.RetentionTime:
    """Fetch a single retention time by ID."""
    retention_time = crud.get_retention_time_by_id(
        db, retention_time_id=retention_time_id
    )
    if retention_time is None:
        raise HTTPException(status_code=404, detail="Retention time not found")
    return retention_time


# Route for the chem_util tools
@router.get(
    "/tools/monoisotopic-mass/",
    tags=[config.STR_TOOLS],
)
def get_mono_isotopic_mass(molecular_formula: str) -> Dict:
    """Calculate monoisotopic mass from a molecular formula."""
    try:
        mass = cu.get_monoisotopic_mass(molecular_formula=molecular_formula)
        return {
            "molecular_formula": molecular_formula,
            "monoisotopic_mass": mass,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/tools/formula-adduct-calc/",
    tags=[config.STR_TOOLS],
)
def get_measured_formula(molecular_formula: str, adduct: str) -> Dict:
    """Get the modified formula when working with adducts like M+H."""
    try:
        molecular_formula = cu.get_measured_formula(
            molecular_formula=molecular_formula, adduct_name=adduct
        )
        return {"measured_formula": molecular_formula, "adduct": adduct}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
