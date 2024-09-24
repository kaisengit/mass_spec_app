#!/usr/bin/env python

import importlib.metadata
import json


def generate_requirements_file(output_file="backend/requirements.txt"):
    # Get a list of all installed packages
    installed_packages = importlib.metadata.distributions()
    # Format as `package==version`
    requirements = sorted(
        [
            f"{pkg.metadata['Name']}=={pkg.version}"
            for pkg in installed_packages
            if "mass-spec-app" not in pkg.metadata["Name"]
        ]
    )

    # Write the requirements to a file
    with open(output_file, "w") as f:
        f.write("\n".join(requirements))

    print(f"requirements.txt file has been created at {output_file}")
    return requirements


def generate_setup_py(
    requirements,
    path_setup="backend/setup.py",
    project_name="mass-spec-app",
    version="0.1",
    author="Kai Kammer",
    author_email="kaikammer@mailbox.org",
    python_min_version="3.12",
):
    # Convert requirements to a valid Python list format for install_requires
    requirements_for_setup = json.dumps(requirements, indent=8)
    # Template for setup.py with dynamic install_requires
    setup_py_content = f"""
from setuptools import setup, find_packages

setup(
    name='{project_name}',
    version='{version}',
    author='{author}',
    python_requires='>={python_min_version}',
    author_email='{author_email}',
    packages=find_packages(),
    install_requires={requirements_for_setup},
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
"""
    # Write the setup.py file
    with open(path_setup, "w") as f:
        f.write(setup_py_content)

    print(f"{path_setup} file has been created.")


def main():
    # Generate both requirements.txt and setup.py
    requirements = generate_requirements_file()
    generate_setup_py(requirements)


if __name__ == "__main__":
    main()
