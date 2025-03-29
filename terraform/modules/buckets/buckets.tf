resource "aws_s3_bucket" "this" {
  bucket = "personal-projects-${local.bucket_name}-${local.env}-${local.aws_region}-${local.aws_account_id}"

  tags = local.tags
}
