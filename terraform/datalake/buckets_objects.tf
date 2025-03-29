# resource "null_resource" "this" {
#   for_each = toset(local.data_sources)
#   triggers = {
#     data_sources = filesha1("./source/${each.value}.json")
#   }
# }

resource "aws_s3_object" "this" {
    # depends_on = [null_resource.this]

    for_each = toset(local.data_sources)

    bucket = "personal-projects-assets-${local.env}-${local.aws_region}-${data.aws_caller_identity.current.account_id}"
    key = "data_sources/${each.value}.json"
    source = "./source/${each.value}.json"
    source_hash = filesha1("./source/${each.value}.json")
}
