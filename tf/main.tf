terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region  = var.region
  profile = "default"
}

terraform {
  backend "s3" {
    bucket = "tfstate-bucket-wiz-task"
    key    = "terraform.tfstate"
    region = "eu-central-1"
  }
}


# create S3 bucket for storing data
module "s3_bucket" {
  source          = "./modules/s3_bucket"
  bucket_name     = var.bucket_name
  lambda_role_arn = aws_iam_role.lambda_role.arn
  tags            = {
    Name        = var.bucket_name
    terraform = "true"
  }
  depends_on = [
    module.lambda,
  ]
}


data "archive_file" "lambda" {
  type             = "zip"
  source_file      = "${path.module}/lambda/main.py"
  output_file_mode = "0666"
  output_path      = "${path.module}/outputs/main.zip"
}

module "lambda" {
  version = "~> 7.20"
  source  = "terraform-aws-modules/lambda/aws"

  function_name = var.lambda_function_name
  handler       = "main.lambda_handler"
  runtime       = "python3.11"
  create_role  = false
  lambda_role      = aws_iam_role.lambda_role.arn
  environment_variables = {
    BUCKET_NAME = var.bucket_name
  }
  publish = true

  allowed_triggers = {
    AllowExecutionFromAPIGateway = {
      service    = "apigateway"
      source_arn = "${module.api_gateway.api_execution_arn}/*/*"
    }
  }

  create_package         = false
  local_existing_package = data.archive_file.lambda.output_path

  tags = {
    terraform = "true"
  }

  depends_on = [
    aws_iam_role.lambda_role,
  ]
}

module "api_gateway" {
  source = "terraform-aws-modules/apigateway-v2/aws"

  name          = var.api_gateway_name
  description   = "API Gateway for Wiz Task"
  protocol_type = "HTTP"

  cors_configuration = {
    allow_headers = ["content-type", "x-amz-date", "authorization", "x-api-key", "x-amz-security-token", "x-amz-user-agent"]
    allow_methods = ["*"]
    allow_origins = ["*"]
  }
  create_domain_name = false

  stage_access_log_settings = null

  routes = {
    "GET /read" = {
      integration = {
        uri                    = module.lambda.lambda_function_invoke_arn
        payload_format_version = "2.0"
      }
    }

    "POST /write" = {
      integration = {
        uri                    = module.lambda.lambda_function_invoke_arn
        payload_format_version = "2.0"
      }
    }
  }

  tags = {
    terraform = "true"
  }
}


# Create IAM role for lambda function
resource "aws_iam_role" "lambda_role" {
  name = var.lambda_function_name

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    terraform = "true"
  }
}

# Attach policy to the role for lambda to access S3 Logs
resource "aws_iam_role_policy_attachment" "lambda_policy_attachment_S3" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}