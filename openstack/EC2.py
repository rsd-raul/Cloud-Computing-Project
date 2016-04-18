from libcloud.compute.types import NodeState
import libcloud.security
from openstack.Connections import Connection


class EC2InstanceOS:

    def __init__(self):
        """ Empty EC2Instance Constructor """

    @staticmethod
    def find_instances_running():
        """ Find EC2 Instances """

        # Disabling SSL certificate validation
        libcloud.security.VERIFY_SSL_CERT = False

        # AWS EC2 Driver
        # driver = Connection.ec2_aws_driver()

        # OpenStack Driver
        driver = Connection.ec2_os_driver()

        # Get all instances associated with this AWS account
        nodes = driver.list_nodes()

        result = []
        for node in nodes:
            if node.state == NodeState.RUNNING:
                result.append(node)

        return result
