from libcloud.compute.types import Provider
from libcloud.compute.types import NodeState
from libcloud.compute.providers import get_driver
from boto import config
import libcloud.security


class EC2InstanceOS:

    def __init__(self):
        """ Empty EC2Instance Constructor """

    @staticmethod
    def find_instances_running():
        """ Find EC2 Instances """

        # Disabling SSL certificate validation
        libcloud.security.VERIFY_SSL_CERT = False

        # AWS EC2 Driver
        # key_id = config.get('Credentials', 'aws_access_key_id')
        # secret_key = config.get('Credentials', 'aws_secret_access_key')
        # aws_driver = get_driver(Provider.EC2_EU_WEST)
        # driver = aws_driver(key_id, secret_key)

        # OpenStack Driver
        key_id = config.get('LibCloud', 'username')
        secret_key = config.get('LibCloud', 'secret_key')
        auth_url = config.get('LibCloud', 'auth_url')

        provider = get_driver(Provider.OPENSTACK)
        driver = provider(key_id, secret_key, ex_force_auth_url=auth_url, ex_force_auth_version='2.0_password',
                          ex_tenant_name=key_id, ex_force_service_region='RegionOne')

        # Get all instances associated with this AWS account
        nodes = driver.list_nodes()

        result = []
        for node in nodes:
            if node.state == NodeState.RUNNING:
                result.append(node)

        return result
