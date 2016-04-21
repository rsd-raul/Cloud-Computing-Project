from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from libcloud.storage.providers import get_driver as get_storage_driver
from libcloud.storage.types import Provider as StorageProvider
from boto import config


class Connection:
    def __init__(self):
        """ Connection Instance """

    @staticmethod
    def ec2_aws_driver():
        """ Obtain and return the Amazon Web Services EC2 Driver for LibCloud """

        # AWS EC2 Driver
        key_id = config.get('Credentials', 'aws_access_key_id')
        secret_key = config.get('Credentials', 'aws_secret_access_key')

        # Obtain the generic driver for the desired provider
        aws_driver = get_driver(Provider.EC2_EU_WEST)

        # Obtain the personalized driver and return it
        driver = aws_driver(key_id, secret_key)

        return driver

    @staticmethod
    def ec2_os_driver():
        """ Obtain and return the OpenStack EC2 Driver for LibCloud """

        key_id = config.get('LibCloud', 'username')
        secret_key = config.get('LibCloud', 'secret_key')
        auth_url = config.get('LibCloud', 'auth_url')

        # Obtain the generic driver for the desired provider
        ec2_driver = get_driver(Provider.OPENSTACK)

        # Obtain the personalized driver and return it
        driver = ec2_driver(key_id, secret_key, ex_force_auth_url=auth_url, ex_force_auth_version='2.0_password',
                            ex_tenant_name=key_id, ex_force_service_region='RegionOne')

        return driver

    @staticmethod
    def s3_aws_driver():
        """ Obtain and return the OpenStack S3 Driver for Amazon Web Services """

        key_id = config.get('Credentials', 'aws_access_key_id')
        secret_key = config.get('Credentials', 'aws_secret_access_key')

        # Obtain the generic driver for the desired provider
        s3_driver = get_storage_driver(StorageProvider.S3_EU_WEST)

        # Obtain the personalized driver and return it
        driver = s3_driver(key_id, secret_key, False)

        return driver

    @staticmethod
    def s3_os_driver():
        """ Obtain and return the OpenStack S3 Driver for LibCloud """

        key_id = config.get('LibCloud', 'username')
        secret_key = config.get('LibCloud', 'secret_key')
        auth_url = config.get('LibCloud', 'auth_url')

        # Obtain the generic driver for the desired provider
        s3_driver = get_storage_driver(StorageProvider.OPENSTACK_SWIFT)

        # Obtain the personalized driver and return it
        driver = s3_driver(key_id, secret_key, ex_force_auth_url=auth_url, ex_force_auth_version='2.0_password',
                           ex_tenant_name=key_id, ex_force_service_region='RegionOne')

        return driver
