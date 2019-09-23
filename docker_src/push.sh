#!/usr/bin/env bash

echo "Start Push"

export DOCKER_URL=asfree/book_crud_api:latest

echo "Docker Push"

docker push $DOCKER_URL

echo "End"

