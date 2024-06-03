#!/usr/bin/env bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )";

cd "$SCRIPT_DIR"

docker-compose build
docker tag consumer_redis-consumer:latest scottzach1/redis-consumer:latest
docker push scottzach1/redis-consumer:latest
