from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    """
    Custom storage backend for handling static files on Amazon S3.
    """
    location = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):
    """
    Custom storage backend for handling media files on Amazon S3.
    """
    location = settings.MEDIAFILES_LOCATION
