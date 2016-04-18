import boto
import boto.ec2
import boto.glacier
from boto import config
from boto.s3.connection import S3Connection
import boto.ec2.cloudwatch
from boto.sdb.regioninfo import SDBRegionInfo
from boto.ec2.autoscale import AutoScaleConnection


class Connection:
    def __init__(self):
        """ Connection Instance """

    @staticmethod
    def ec2_connection():
        """ Create and return an EC2 Connection """
        conn = boto.ec2.connect_to_region('eu-west-1')
        return conn

    @staticmethod
    def s3_connection():
        """ Create and return an EC3 Connection """
        conn = S3Connection()
        return conn

    @staticmethod
    def cw_connection():
        """ Create and return an CW Connection """
        conn = boto.connect_cloudwatch()

        return conn

    @staticmethod
    def sns_connection():
        """ Create and return an SNS Connection """

        key_id = config.get('Credentials', 'aws_access_key_id')
        access_key = config.get('Credentials', 'aws_secret_access_key')

        # Undocumented way to connect SNS to a different zone... Appears to work
        region_name = 'eu-west-1'
        region_endpoint = 'sns.eu-west-1.amazonaws.com'
        region = SDBRegionInfo(None, region_name, region_endpoint)
        conn = boto.connect_sns(key_id, access_key, region=region)

        return conn

    @staticmethod
    def glacier_connection():
        """ Create and return a Glacier Connection """

        conn = boto.glacier.connect_to_region('eu-west-1')

        return conn

    @staticmethod
    def as_connection():

        # Deprecated by using anotation in boto.config
        # import boto.ec2.autoscale
        # auto_scale = boto.ec2.autoscale.connect_to_region('eu-west-1')

        key_id = config.get('Credentials', 'aws_access_key_id')
        access_key = config.get('Credentials', 'aws_secret_access_key')

        conn = AutoScaleConnection(key_id, access_key)

        return conn
