#!/bin/sh

# do not do this in production
echo "Running Alembic migrations..."
alembic upgrade head

# Check the first argument to determine the mode
if [ "$1" = 'debug' ]; then
  echo "Starting the app in debug mode..."
  exec python -m debugpy --wait-for-client --listen 0.0.0.0:5678 -m uvicorn mass_spec_app:app --host 0.0.0.0 --port 8255
else
  echo "Starting the app in normal mode..."
  exec gunicorn --bind 0.0.0.0:8255 -k uvicorn.workers.UvicornWorker mass_spec_app:app
fi
