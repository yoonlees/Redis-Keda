#!/usr/bin/env bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )";

cd "$SCRIPT_DIR"

docker-compose build
docker tag publisher_redis-publisher:latest scottzach1/redis-publisher:latest
docker push scottzach1/redis-publisher:latest
