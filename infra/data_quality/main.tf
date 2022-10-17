####################################################
# Lambda Function
####################################################
resource "aws_lambda_function" "great_expectations_lambda" {
  function_name = "${var.aws_account_id}-great-expectations-lambda"
  role          = aws_iam_role.great_expectations_lambda_role.arn
  memory_size   = 512
  timeout       = 900 # 15 minutes
  package_type  = "Image"
  image_uri     = "${var.aws_account_id}.dkr.ecr.${var.aws_region}.amazonaws.com/great-expectations-images"
}

####################################################
# IAM Role
####################################################
resource "aws_iam_role" "great_expectations_lambda_role" {
  name = "${var.aws_environment}-great-expectations-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = ""
        Effect = "Allow"
        Action = "sts:AssumeRole"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

####################################################
# IAM Policy
####################################################
resource "aws_iam_role_policy" "great_expectations_lambda_role_policy" {
  name = "${var.aws_environment}-great-expectations-lambda-role-policy"
  role = aws_iam_role.great_expectations_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = ""
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = [
          "arn:aws:logs:${var.aws_region}:${var.aws_account_id}:*",
          "${aws_cloudwatch_log_group.great_expectations_lambda_cloudwatch_log_group.arn}:*"
        ]
      }
    ]
  })
}

####################################################
# Cloudwatch Log Group
####################################################
resource "aws_cloudwatch_log_group" "great_expectations_lambda_cloudwatch_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.great_expectations_lambda.function_name}"
  retention_in_days = 14
}