from libcloud.storage.providers import get_driver as get_storage_driver
from libcloud.storage.types import Provider as StorageProvider
from boto import config
import libcloud.security


class S3BucketOS:
    def __init__(self):
        """ S3Bucket Constructor """

    @staticmethod
    def list_buckets():

        # AWS Driver
        # s3_driver = get_storage_driver(StorageProvider.S3_EU_WEST)

        # key_id = config.get('Credentials', 'aws_access_key_id')
        # secret_key = config.get('Credentials', 'aws_secret_access_key')

        # s3_storage = s3_driver(key_id, secret_key, False)

        # OpenStack Driver
        s3_driver = get_storage_driver(StorageProvider.OPENSTACK_SWIFT)

        key_id = config.get('LibCloud', 'username')
        secret_key = config.get('LibCloud', 'secret_key')
        auth_url = config.get('LibCloud', 'auth_url')

        libcloud.security.VERIFY_SSL_CERT = False

        s3_storage = s3_driver(key_id, secret_key, ex_force_auth_url=auth_url, ex_force_auth_version='2.0_password',
                               ex_tenant_name=key_id, ex_force_service_region='RegionOne')

        """ List S3 buckets """
        buckets = s3_storage.list_containers()

        return buckets

    @staticmethod
    def store_in_bucket(bucket, file_title, file_location):
        """ Store a file inside a Bucket """

        bucket.upload_object(file_location, file_title)
