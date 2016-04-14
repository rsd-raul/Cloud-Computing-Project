import boto
import boto.ec2
from boto.s3.connection import S3Connection
import boto.ec2.cloudwatch


class Connection:
    def __init__(self):
        """ Connection Instance """
        self.region = 'eu-west-1'

    def ec2_connection(self):
        """ Create and return an EC2 Connection """
        conn = boto.ec2.connect_to_region(self.region)
        return conn

    @staticmethod
    def s3_connection():
        """ Create and return an EC3 Connection """
        conn = S3Connection()
        return conn

    @staticmethod
    def cw_connection():
        """ Create and return an EC3 Connection """
        conn = boto.connect_cloudwatch()
        # Price by region only supports us-east-1
        # conn = boto.ec2.cloudwatch.connect_to_region("us-east-1")
        return conn
