#!/bin/bash

docker compose exec -it backend /app/backend/scripts/admin.py "$@"
