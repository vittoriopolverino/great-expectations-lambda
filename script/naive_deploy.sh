#!/usr/bin/env bash

# env var or default
ACCOUNT_ID="${AWS_ACCOUNT_ID:-111111111111}"
REGION=eu-west-1


docker_login_to_ecr() {
  aws configure set aws_access_key_id  $AWS_ACCESS_KEY
  aws configure set aws_secret_access_key  $AWS_SECRET_KEY
  aws configure set region $REGION
  aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
}

docker_tag() {
  docker tag great-expectations-images:latest $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/great-expectations-images
}

docker_push() {
  docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/great-expectations-images
}

update_lambda_function() {
  aws lambda update-function-code --region $REGION --function-name your-lambda-name --image-uri $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/great-expectations-images
}

docker_login_to_ecr
docker_tag
docker_push
update_lambda_function

$SHELL
