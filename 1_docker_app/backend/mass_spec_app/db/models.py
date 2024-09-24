# 2024-09 Kai-Michael Kammer
"""
Defines SQLAlchemy models that map to database tables, including the
Compound, MeasuredCompound, RetentionTime, and Adduct models.
These models represent the structure of the application's database and
include relationships between tables.
"""
from typing import List, Optional

from mass_spec_app.db.session import Base
from sqlalchemy import (Boolean, CheckConstraint, Column, DateTime, Float,
                        ForeignKey, Integer, String, UniqueConstraint)
from sqlalchemy.orm import Mapped, mapped_column, relationship


# check if the inital migration was done
class InitializationStatus(Base):
    __tablename__ = "initialization_status"

    id = Column(Integer, primary_key=True, index=True)
    is_initialized = Column(
        Boolean, default=False
    )  # Flag to check if DB is initialized
    initialized_at = Column(DateTime, default=None)  # Timestamp when it was initialized


class Compound(Base):
    __tablename__ = "compounds"

    compound_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    compound_name: Mapped[str] = mapped_column(String, index=True)
    molecular_formula: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    type: Mapped[str] = Column(String, nullable=True)  # Allow NULL values in 'type'
    computed_mass: Mapped[float] = mapped_column(Float)

    # One-to-Many relationship with MeasuredCompound (Optional for reverse relationship)
    measured_compounds: Mapped[List["MeasuredCompound"]] = relationship(
        "MeasuredCompound", back_populates="compound"
    )


class Adduct(Base):
    __tablename__ = "adducts"

    adduct_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    adduct_name: Mapped[str] = mapped_column(String)
    mass_adjustment: Mapped[float] = mapped_column(Float)
    ion_mode: Mapped[str] = mapped_column(String)

    # One-to-Many relationship with MeasuredCompound
    measured_compounds: Mapped[List["MeasuredCompound"]] = relationship(
        "MeasuredCompound", back_populates="adduct"
    )


class RetentionTime(Base):
    __tablename__ = "retention_times"

    retention_time_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )
    retention_time: Mapped[float] = mapped_column(Float)
    comment: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # One-to-Many relationship with MeasuredCompound
    measured_compounds: Mapped[List["MeasuredCompound"]] = relationship(
        "MeasuredCompound", back_populates="retention_time"
    )
    # check that retention_time is positive
    __table_args__ = (
        CheckConstraint("retention_time > 0", name="ck_retention_time_positive"),
    )


class MeasuredCompound(Base):
    __tablename__ = "measured_compounds"

    measured_compound_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )
    compound_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("compounds.compound_id")
    )
    adduct_id: Mapped[int] = mapped_column(Integer, ForeignKey("adducts.adduct_id"))
    retention_time_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("retention_times.retention_time_id")
    )
    measured_mass: Mapped[float] = mapped_column(Float)
    molecular_formula: Mapped[str] = mapped_column(String)

    # Many-to-One relationships
    compound: Mapped["Compound"] = relationship(
        "Compound", back_populates="measured_compounds"
    )
    adduct: Mapped["Adduct"] = relationship(
        "Adduct", back_populates="measured_compounds"
    )
    retention_time: Mapped["RetentionTime"] = relationship(
        "RetentionTime", back_populates="measured_compounds"
    )
    # Ensure uniqueness across compound_id, retention_time, and adduct_id
    __table_args__ = (
        UniqueConstraint(
            "compound_id",
            "retention_time_id",
            "adduct_id",
            name="uq_compound_retention_adduct",
        ),
    )
