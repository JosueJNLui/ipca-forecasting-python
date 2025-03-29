variable "env" {
  description = "Execution environment"
  type        = string
}

variable "aws_region" {
  description = "AWS Region"
  type        = string
}

variable "aws_account_id" {
  description = "Account ID from AWS account"
  type        = string
}

variable "bucket_name" {
  description = "Bucket's name"
  type        = string
}

variable "tags" {
  description = "Tags to be attached to the resource"
  type        = map(string)
}
