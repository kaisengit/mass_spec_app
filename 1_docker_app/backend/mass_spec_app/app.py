# 2024-09 Kai-Michael Kammer
"""
Main FastAPI application file that defines the API routes for managing compounds and measured-compounds.
Handles the startup, shutdown, and routing of requests to the appropriate endpoints for database interactions.
"""  # noqa: E501
from contextlib import asynccontextmanager

from fastapi import FastAPI
from mass_spec_app.api.routes import router
from mass_spec_app.db.session import SessionLocal
from mass_spec_app.scripts.populate_data import populate_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Manually create the database session as lifespan does not work with Depends # noqa: E501
    db = SessionLocal()
    try:
        # Run the data population logic
        populate_data(
            db
        )  # Pass the session manually to the populate_data function
        yield
    finally:
        # Close the database session
        db.close()


app = FastAPI(
    servers=[{"url": "/", "description": "Mass Spec App API"}],
    docs_url="/api/docs",
    redoc_url=None,
    openapi_url="/api",
    title="Mass Spec App",
    swagger_ui_parameters={"tryItOutEnabled": True},
    separate_input_output_schemas=False,
    lifespan=lifespan,
)

# include api routes
app.include_router(router=router)

# Create all database tables
# we are using alembic instead
# models.Base.metadata.create_all(bind=engine)
