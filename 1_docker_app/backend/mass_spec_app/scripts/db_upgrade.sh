#!/bin/sh
# Script to apply the latest Alembic migrations
echo "Running Alembic migrations..."
alembic upgrade head
