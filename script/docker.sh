#!/usr/bin/env bash

LOCAL_PATH=C:/great_expectations_local_site/

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
  echo "Invoking the lambda function in the container . . ."
  winpty docker exec -it lambda-container bash -c "python src/lambda_function_local.py"
}

copy_ge_local_site() {
  echo "Copying the great expectations local site in $LOCAL_PATH . . ."
  docker cp lambda-container:/var/task/great_expectations/uncommitted/data_docs/local_site $LOCAL_PATH
}

docker_build
docker_run
docker_exec
copy_ge_local_site

$SHELL
