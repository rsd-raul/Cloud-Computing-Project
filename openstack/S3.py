from libcloud.storage.providers import get_driver as get_storage_driver
from libcloud.storage.types import Provider as StorageProvider
from boto import config

class S3BucketOS:
    def __init__(self):
        """ S3Bucket Constructor """

    @staticmethod
    def list_buckets():
        s3_driver = get_storage_driver(StorageProvider.S3_EU_WEST)

        key_id = config.get('Credentials', 'aws_access_key_id')
        secret_key = config.get('Credentials', 'aws_secret_access_key')
        s3_storage = s3_driver(key_id, secret_key, False)

        """ List S3 buckets """
        buckets = s3_storage.list_containers()

        return buckets


