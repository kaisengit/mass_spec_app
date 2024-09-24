#!/bin/bash

docker exec -it ${DB_CONTAINER_NAME} sh ./scripts/db_revision.sh "$1"
