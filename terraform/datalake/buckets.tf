module "buckets" {
  source         = "../modules/buckets"
  for_each       = toset(local.buckets)
  env            = local.env
  aws_region     = local.aws_region
  aws_account_id = data.aws_caller_identity.current.account_id
  bucket_name    = each.value
  tags = {
    "project_name"       = local.project
    "projects_component" = local.projects_component
  }
}
