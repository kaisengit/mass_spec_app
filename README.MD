# Mass Spec App
## Manage mass spec data via restAPI
### 2024-09 Kai-Michael Kammer
0_initial_explore_data just contains a Jupyter notebook for having a first look at the data.

The main app is found 1_docker_app. It is using postgresql as a database, caddy as a reverse proxy/load balancer and Python/SQLAlchemy/FastAPI as a backend.

## Installation
Simpy start the application with

    docker compose up -d --build

There is also a docker-compose.dev.yml file allowing for attaching a debugger. A debug configuration for vscode is included in .vscode.
The debug configuration does NOT build the image defined in the Dockerfile but rather passes through all backend files via a volumen. Therfore code changes are directly effective (or after restarting the app).

Note that the project uses pre-commit hooks to maintain properly formatted code. Therefore the package pre-commit

## Usage
The web frontend will be served on mass-spec-app.localhost.
The address may be configured in the Caddyfile.txt

Note that at the moment the database does not use a persistent volume; restarting via docker compose means also restarting with a clean database.
