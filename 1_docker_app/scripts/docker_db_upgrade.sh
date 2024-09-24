#!/bin/bash

docker exec -it ${DB_CONTAINER_NAME} sh ./scripts/db_upgrade.sh
