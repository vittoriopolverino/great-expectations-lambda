#!/usr/bin/env bash

ACCOUNT_ID=111111111111
REGION=eu-west-1

docker_tag() {
  docker tag great-expectations-images:latest $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/great-expectations-images
}

docker_push() {
  docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/great-expectations-images
}

update_lambda_function() {
  aws lambda update-function-code --region $REGION --function-name your-lambda-name --image-uri $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/great-expectations-images
}

docker_tag
docker_push
update_lambda_function

$SHELL
