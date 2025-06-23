variable "region" {
  type    = string
  default = "eu-central-1"
}

variable "lambda_function_name" {
  type    = string
  default = "wiz-task-lambda"
}

variable "bucket_name" {
  type    = string
  default = "wiz-task-bucket"
}

variable "api_gateway_name" {
  type    = string
  default = "wiz-task-api-gateway"
}