#!/usr/bin/env bash

echo "Start Build"

export GIT_CLONE=https://github.com/artemzdor/Book_Crud_Api.git
export DOCKER_URL=asfree/book_crud_api:latest

echo "Git Clone: book_crud_api"

git clone $GIT_CLONE

echo "Docker Build"

docker build -t $DOCKER_URL .

echo "End"
