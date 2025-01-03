"""Initial migration

Revision ID: b36958980c56
Revises:
Create Date: 2024-09-23 19:41:43.689194

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b36958980c56"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "adducts",
        sa.Column("adduct_id", sa.Integer(), nullable=False),
        sa.Column("adduct_name", sa.String(), nullable=False),
        sa.Column("mass_adjustment", sa.Float(), nullable=False),
        sa.Column("ion_mode", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("adduct_id"),
    )
    op.create_index(
        op.f("ix_adducts_adduct_id"), "adducts", ["adduct_id"], unique=False
    )
    op.create_table(
        "compounds",
        sa.Column("compound_id", sa.Integer(), nullable=False),
        sa.Column("compound_name", sa.String(), nullable=False),
        sa.Column("molecular_formula", sa.String(), nullable=False),
        sa.Column("type", sa.String(), nullable=True),
        sa.Column("computed_mass", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("compound_id"),
    )
    op.create_index(
        op.f("ix_compounds_compound_id"), "compounds", ["compound_id"], unique=False
    )
    op.create_index(
        op.f("ix_compounds_compound_name"), "compounds", ["compound_name"], unique=False
    )
    op.create_table(
        "initialization_status",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("is_initialized", sa.Boolean(), nullable=True),
        sa.Column("initialized_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_initialization_status_id"),
        "initialization_status",
        ["id"],
        unique=False,
    )
    op.create_table(
        "retention_times",
        sa.Column("retention_time_id", sa.Integer(), nullable=False),
        sa.Column("retention_time", sa.Float(), nullable=False),
        sa.Column("comment", sa.String(), nullable=True),
        sa.CheckConstraint("retention_time > 0", name="ck_retention_time_positive"),
        sa.PrimaryKeyConstraint("retention_time_id"),
    )
    op.create_index(
        op.f("ix_retention_times_retention_time_id"),
        "retention_times",
        ["retention_time_id"],
        unique=False,
    )
    op.create_table(
        "measured_compounds",
        sa.Column("measured_compound_id", sa.Integer(), nullable=False),
        sa.Column("compound_id", sa.Integer(), nullable=False),
        sa.Column("adduct_id", sa.Integer(), nullable=False),
        sa.Column("retention_time_id", sa.Integer(), nullable=False),
        sa.Column("measured_mass", sa.Float(), nullable=False),
        sa.Column("molecular_formula", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["adduct_id"],
            ["adducts.adduct_id"],
        ),
        sa.ForeignKeyConstraint(
            ["compound_id"],
            ["compounds.compound_id"],
        ),
        sa.ForeignKeyConstraint(
            ["retention_time_id"],
            ["retention_times.retention_time_id"],
        ),
        sa.PrimaryKeyConstraint("measured_compound_id"),
        sa.UniqueConstraint(
            "compound_id",
            "retention_time_id",
            "adduct_id",
            name="uq_compound_retention_adduct",
        ),
    )
    op.create_index(
        op.f("ix_measured_compounds_measured_compound_id"),
        "measured_compounds",
        ["measured_compound_id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_measured_compounds_measured_compound_id"),
        table_name="measured_compounds",
    )
    op.drop_table("measured_compounds")
    op.drop_index(
        op.f("ix_retention_times_retention_time_id"), table_name="retention_times"
    )
    op.drop_table("retention_times")
    op.drop_index(
        op.f("ix_initialization_status_id"), table_name="initialization_status"
    )
    op.drop_table("initialization_status")
    op.drop_index(op.f("ix_compounds_compound_name"), table_name="compounds")
    op.drop_index(op.f("ix_compounds_compound_id"), table_name="compounds")
    op.drop_table("compounds")
    op.drop_index(op.f("ix_adducts_adduct_id"), table_name="adducts")
    op.drop_table("adducts")
    # ### end Alembic commands ###
