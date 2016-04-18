import libcloud.security
from openstack.Connections import Connection


class S3BucketOS:
    def __init__(self):
        """ S3Bucket Constructor """

    @staticmethod
    def list_buckets():

        libcloud.security.VERIFY_SSL_CERT = False

        # AWS S3 Driver
        # driver = Connection.s3_aws_driver()

        # OpenStack S3 Driver
        driver = Connection.s3_os_driver()

        """ List S3 buckets """
        buckets = driver.list_containers()

        return buckets

    @staticmethod
    def store_in_bucket(bucket, file_title, file_location):
        """ Store a file inside a Bucket """

        bucket.upload_object(file_location, file_title)
