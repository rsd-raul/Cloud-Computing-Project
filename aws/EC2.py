from boto import exception
from boto import config


class EC2Instance:

    def __init__(self):
        """ Empty EC2Instance Constructor """

    @staticmethod
    def find_instances_running(conn):
        """ Find EC2 Instances """

        # Get all instance reservations associated with this AWS account
        reservations = conn.get_all_reservations()

        # Iterate over all the instances inside all the reservations and return the ones running
        result = []
        for res in reservations:
            for instance in res.instances:
                if instance.state == u'running':
                    result.append(instance)

        return result

    @staticmethod
    def find_instances_running_zone(conn, zone):
        """ Find EC2 Instances """

        # Iterate over all the instances inside all the reservations and return the ones running in the requested zone
        result = []
        for res in conn.get_all_reservations():
            for instance in res.instances:
                if instance.state == u'running' and instance.placement == zone:
                    result.append(instance)

        return result

    @staticmethod
    def create_instance_with_ami(conn, ami):
        """ Create a new instance based on AMI"""

        # Start an instance with the desired ami, in this case I decided to hard code the type to a free tier machine
        conn.run_instances(ami, key_name=config.get('Credentials', 'key_name'), instance_type="t2.micro")

    @staticmethod
    def create_instance_with_so(conn, so):
        """ Create a new instance based on AMI"""

        # Select the AMI corresponding with Windows or Linux depending on the user
        ami = "ami-c6972fb5" if so == "windows" else "ami-f95ef58a"

        # Start an instance with the calculated ami, in this case I decided to hard code the type to a free tier machine
        conn.run_instances(ami, key_name=config.get('Credentials', 'key_name'), instance_type="t2.micro")

    @staticmethod
    def start_instance(conn, instance_id):
        """ Starts a stopped instance """

        conn.start_instances(instance_id, False)

    @staticmethod
    def stop_instances(conn):
        """ Stops all running instances"""

        # From all the running instances, extract the id and make a list
        instances_ids = [instance.id for instance in EC2Instance.find_instances_running(conn)]

        # If 1 or more instances are running, notify the user and stop them all
        if len(instances_ids) > 0:
            for instance_id in instances_ids:
                print "Stopping instance with id:", instance_id

            # Stop all the running instances
            conn.stop_instances(instances_ids, False)

        # If there is nothing running, warn the user
        else:
            print "Nothing running"

    @staticmethod
    def stop_instance(conn, instance_id):
        """ Stops a running instance"""

        # Stop the instance the user requested and notify the user of the result
        try:
            stopped = conn.stop_instances(instance_id, False)
            print "Stopping instance with id:", stopped[0].id

        except exception.EC2ResponseError:
            print "Incorrect id format, try again"

    @staticmethod
    def terminate_instance(conn, instance_id):
        """ Terminate a running or stopped instance"""

        # Terminate an instance based on a user provided id
        conn.terminate_instances(instance_id)

    @staticmethod
    def terminate_all_instances(conn):
        """ Terminate all instances"""

        # Retrieve all the ids for the running instances from all the reservations
        not_terminated = []
        for reservation in conn.get_all_instances():
            for inst in reservation.instances:
                print inst.id, inst.state, inst.public_dns_name
                if inst.state != u'terminated':
                    not_terminated.append(inst.id)

        # If there are running instances, terminate them, if not, notify the user
        if len(not_terminated) > 0:
            print "\nTerminating instances ", not_terminated
            conn.terminate_instances(instance_ids=not_terminated)
        else:
            print "Nothing to terminate"
