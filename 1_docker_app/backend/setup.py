from setuptools import find_packages, setup

setup(
    name="mass-spec-app",
    version="0.1",
    author="Kai Kammer",
    python_requires=">=3.12",
    author_email="kaikammer@mailbox.org",
    packages=find_packages(),
    install_requires=[
        "Jinja2==3.0.3",
        "SQLAlchemy==2.0.35",
        "alembic==1.13.3",
        "annotated-types==0.7.0",
        "molmass==2024.5.24",
        "numpy==2.1.1",
        "openpyxl==3.1.5",
        "packaging==24.1",
        "pandas==2.2.3",
        "psycopg-binary==3.2.2",
        "psycopg-pool==3.2.3",
        "psycopg==3.2.2",
        "pydantic==2.9.2",
        "pydantic_core==2.23.4",
        "starlette==0.38.6",
        "uvicorn==0.30.6",
        "gunicorn==23.0.0",
        "fastapi==0.115.0",
    ],
    extras_require={
        "dev": [
            "mypy==1.11.2",
            "debugpy==1.8.5",
            "black==24.8.0",
            "flake8==7.1.1",
            "isort==5.13.2",
            "pre-commit==3.8.0",
            "types-passlib==1.7.7.20240819",
            "types-requests==2.32.0.20240914",
            "types-setuptools==75.1.0.20240917",
            "celery-types==0.22.0",
            "types-setuptools==75.1.0.20240917",
            "sqlalchemy[mypy]",
            "prettyprinter==0.18.0",
        ],
        "test": [
            "pytest==8.3.3",
            "pytest-cov==5.0.0",
            "mock==5.1.0",
            "fastapi[testclient]",
            "SQLAlchemy-Utils==0.41.2",
            "httpx==0.27.2",
        ],
    },
)