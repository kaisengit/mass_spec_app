#!/bin/sh
# Script to generate a new Alembic migration based on the current models
if [ -z "$1" ]
then
  echo "You need to provide a migration message!"
  echo "Usage: ./scripts/db_revision.sh 'Add new column to table'"
  exit 1
fi

echo "Generating a new Alembic migration with message: '$1'"
alembic revision --autogenerate -m "$1"
