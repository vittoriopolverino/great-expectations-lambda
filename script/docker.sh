#!/usr/bin/env bash

docker_build() {
  echo "Building docker image . . . "
  docker stop lambda-container
  docker rm lambda-container
  docker rmi lambda-container-image:latest
  docker build -t lambda-container-image .
}

docker_run() {
  echo "Running the docker container . . ."
  docker run -d --name lambda-container lambda-container-image:latest
}

docker_exec() {
  echo "Running the lambda function . . ."
  winpty docker exec -it lambda-container bash -c "python src/lambda_function_local.py"
}

docker_build
docker_run
docker_exec

$SHELL
