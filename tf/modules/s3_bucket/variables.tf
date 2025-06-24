variable "bucket_name" {
  type    = string
  default = null
}

variable "lambda_role_arn" {
  type    = string
  default = null
}

variable "tags" {
  type    = map(string)
  default = null
}