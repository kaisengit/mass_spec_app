# 2024-09 Kai-Michael Kammer
"""
Defines Pydantic schemas for data validation and serialization of request/response payloads.
Schemas are used for ensuring valid input when interacting with compounds, measured-compounds, retention times, and adducts.
They are split into three parts—Base (common to all), Create (POST), and Response (GET, which includes auto-generated fields).
"""  # noqa: E501
from typing import Optional

from pydantic import BaseModel


# Adduct Schema
class AdductBase(BaseModel):
    adduct_name: str
    mass_adjustment: float
    ion_mode: str


class AdductCreate(AdductBase):
    pass  # No additional fields required for creating an adduct


class Adduct(AdductBase):
    adduct_id: int

    class Config:
        from_attributes = True  # allows Pydantic to extract data from SQLAlchemy objects using their attributes # noqa: E501


# Compound Schema
class CompoundBase(BaseModel):
    compound_id: int
    compound_name: str
    molecular_formula: str
    type: Optional[str] = None  # Make 'type' field optional to allow None


class CompoundCreate(CompoundBase):
    pass


class Compound(CompoundBase):
    computed_mass: float  # This will be computed using RDKit

    class Config:
        from_attributes = True  # allows Pydantic to extract data from SQLAlchemy objects using their attributes # noqa: E501


# Retention Time Schema
class RetentionTimeBase(BaseModel):
    retention_time: float


class RetentionTimeCreate(RetentionTimeBase):
    comment: Optional[str] = None


class RetentionTime(RetentionTimeBase):
    retention_time_id: int
    comment: Optional[str] = None

    class Config:
        from_attributes = True  # allows Pydantic to extract data from SQLAlchemy objects using their attributes # noqa: E501


# Measured Compound Schema
class MeasuredCompoundBase(BaseModel):
    pass


class MeasuredCompoundCreate(MeasuredCompoundBase):
    compound_id: int
    retention_time: float
    adduct_name: str
    retention_time_comment: Optional[str] = None


class MeasuredCompound(MeasuredCompoundBase):
    measured_compound_id: int
    measured_mass: float  # Measured mass will be calculated based on the adduct
    molecular_formula: str  # formula is computed based on adduct
    retention_time_id: int  # is looked up
    adduct_id: int  # will be found by DB lookup
    compound: Compound
    retention_time: RetentionTime
    adduct: Adduct

    class Config:
        from_attributes = True  # allows Pydantic to extract data from SQLAlchemy objects using their attributes # noqa: E501
