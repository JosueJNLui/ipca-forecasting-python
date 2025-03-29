locals {
  env                = var.env
  aws_region         = var.aws_region
  aws_profile        = var.aws_profile
  project            = var.project
  projects_component = var.projects_component


  buckets = ["assets", "landing", "bronze", "silver", "gold"]
}
