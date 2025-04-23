import boto3
import boto3.session


def list_bucket_objects(
    aws_profile: str, aws_region: str, bucket_name: str, dir_name: str
) -> list:
    client = boto3.Session(profile_name=aws_profile, region_name=aws_region)
    s3 = client.resource("s3")
    bucket = s3.Bucket(bucket_name)

    return [
        object_summary.key
        for object_summary in bucket.objects.filter(Prefix=f"{dir_name}/")
    ]
