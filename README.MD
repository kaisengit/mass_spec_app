# Mass Spec App
## Manage mass spec data via restAPI
### 2024-09 Kai-Michael Kammer
0_initial_explore_data just contains a Jupyter notebook for having a first look at the data.


The main app is found 1_docker_app. It is using postgresql as a database, caddy as a reverse proxy/load balancer and Python/SQLAlchemy/FastAPI as a backend.
![App Overview](https://github.com/kaisengit/mass_spec_app/blob/master/images/app_overview.png?raw=true)
## Installation
First get Docker for your operating system: https://www.docker.com/

Then, simply start the application with (inside the 1_docker_app/ folder)

    docker compose up -d --build


This will bring up three docker containers: caddy, postgresql and the main mass-spec-app.

You can remove all containers with

    docker compose down

in the same folder.

There is also a docker-compose.dev.yml file allowing for attaching a debugger. A debug configuration for vscode is included in .vscode.
The debug configuration does NOT build the image defined in the Dockerfile but rather passes through all backend files via a volumee. Therefore, code changes are directly effective (or after restarting the app). Bring it up with:

    docker compose up -f docker-compose.dev.yml -d --build

Note that the project uses pre-commit hooks to maintain properly formatted code. Therefore the package pre-commit is required for committing.
Unit tests via pytest should be run from within the docker container (working database connection required).

## Input Data
Data is required to be in the 1_docker_app/migration/ folder (adducts.json, compounds.xlsx, measured-compounds.xlsx).

## Usage
The web frontend will be served by caddy on mass-spec-app.localhost.
The address may be configured in the Caddyfile.txt

Click on the link to go to the Swagger UI. This provides a comfortable web frontend for the api.
All API functions, including their description and expected types, are available here.

Note that at the moment the database does not use a persistent volume; restarting via docker compose means also restarting with a clean database.

## Database Model
![App Overview](https://github.com/kaisengit/mass_spec_app/blob/master/images/db_model.png?raw=true)
