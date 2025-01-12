from storages.backends.s3boto3 import S3Boto3Storage
from storages.utils import setting


class StaticStorage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"
    custom_domain = (
        f"{setting('AWS_S3_CUSTOM_DOMAIN')}/{setting('AWS_STORAGE_BUCKET_NAME')}"
    )


class MediaStorage(S3Boto3Storage):
    location = "media"
    default_acl = "public-read"
    custom_domain = (
        f"{setting('AWS_S3_CUSTOM_DOMAIN')}/{setting('AWS_STORAGE_BUCKET_NAME')}"
    )
    file_overwrite = False
