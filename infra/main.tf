terraform {
  backend "s3" {}
}

provider "aws" {
  allowed_account_ids = [var.aws_account_id]
  region              = var.aws_region
}

####################################################
# Dynamic Glue Partitions
####################################################
module "dynamic_glue_partitions" {
  source         = "./dynamic_glue_partitions"
  aws_account_id = var.aws_account_id
  aws_region     = var.aws_region
  environment    = var.environment
}

####################################################
# Monitoring
####################################################
module "monitoring" {
  source      = "./monitoring"
  environment = var.environment
}
