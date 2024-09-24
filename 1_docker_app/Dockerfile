# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12-slim

# EXPOSE 8255

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app
# the whole app
COPY ./backend/ /app/
# the initial files for data migration
COPY ./migration/ /app/migration/
# the homepage html
COPY ./templates/ /app/templates/
# alembic
COPY alembic.ini /app/
COPY ./alembic /app/alembic
# Copy and make the shell script executable
COPY ./scripts/docker_entrypoint.sh /app
RUN chmod +x /app/docker_entrypoint.sh

# install app
RUN pip install --upgrade pip
RUN python -m pip install -e /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser


# Use the entrypoint script to manage Alembic and start the app
ENTRYPOINT ["/app/docker_entrypoint.sh"]
