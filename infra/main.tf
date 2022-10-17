terraform {
  backend "s3" {}
}

provider "aws" {
  allowed_account_ids = [var.aws_account_id]
  region              = var.aws_region
}

####################################################
# Data Quality - Great Expecations
####################################################
module "data_quality" {
  source         = "./data_quality"
  aws_account_id = var.aws_account_id
  aws_region     = var.aws_region
  environment    = var.environment
}
