terraform {
  backend "s3" {
    encrypt        = true
    bucket         = "josu-personal-projects-us-east-2"
    dynamodb_table = "josu-personal-projects-tfstate-dynamo"
    key            = "ipca-forecasting/datalake/terraform.tfstate"
    region         = "us-east-2"
    profile        = "dev"
  }
}
