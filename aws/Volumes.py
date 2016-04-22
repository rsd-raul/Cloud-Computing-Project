from boto import exception
from boto import config


class Volumes:
    def __init__(self):
        """ Volumes Constructor """

    @staticmethod
    def list_volumes(conn):
        """ Lists volumes from an AWS account """

        # Get all volumes
        vols = conn.get_all_volumes()

        # If volumes found, return them
        if vols:
            return vols

            # Deprecated code

            # # Loop through volumes
            # for v in vols:
            #     print 'Volume Id:', v.id
            #     print 'Volume Status:', v.status
            #     print 'Volume Size:', v.size
            #     print 'Zone:', v.zone
            #     print 'Volume Type:', v.type
            #
            #     # Print attachment set object
            #     attachment_data = v.attach_data
            #     print 'Instance Id:', attachment_data.instance_id
            #     print 'Attached Time:', attachment_data.attach_time
            #     print 'Device:', attachment_data.device

        # If not, notify the user
        else:
            print 'No volumes found'

    @staticmethod
    def attach_volume(conn, volume_id, instance_id):
        """ Attaches a volume to an EC2 instance """

        # Loop through volumes to find the matching one (by id)
        volume = None
        for vol in conn.get_all_volumes():
            if vol.id == volume_id:
                volume = vol

        # If there is no volume with that id, warn the user
        if volume is None:
            print "No volume with that id"
            return False

        # If the status of the volume is not available (needs to be in order to attach), warn the user
        if volume.status != "available":
            print "Volume in use"
            return False

        # Attach the volume to the instance by id
        result = volume.attach(instance_id, '/dev/sdh')

        # Notify the user about the result of the attachment process
        if result:
            print 'Volume ', volume_id, ' attached successfully to instance', instance_id, '\n'
            return True
        else:
            print 'There`s an error attaching the volume ', volume_id, 'to the instance ', instance_id
            return False

    @staticmethod
    def detach_volume(conn, volume_id):
        """ Detaches a specific volume from its instance"""

        # Loop through volumes to find the matching one (by id)
        volume = None
        for vol in conn.get_all_volumes():
            if vol.id == volume_id:
                volume = vol

        # If there is no volume with that id, warn the user
        if volume is None:
            print "No volume with that id"
            return False

        # If the status of the volume is not in use (needs to be in order to detach), warn the user
        if volume.status != "in-use":
            print "Volume in not attached"
            return False

        try:
            # Detach the volume and inform the user
            result = volume.detach()
            if result:
                print 'Volume ', volume_id, ' detached successfully\n'
                return True

        # If problems arise, warn the user
        except exception.EC2ResponseError:
            print "There's an error detaching the volume", volume_id
            return False

    @staticmethod
    def create_volume(conn):
        """ Creating a new volume """

        try:
            # Create a 30gb volume of type gp2 with the region eu-west-1a
            conn.create_volume(30, config.get('Credentials', 'region')+"a", None, "gp2")
            return True

        # If problems arise, warn the user
        except exception.EC2ResponseError:
            print "Problems creating volume"
            return False

    @staticmethod
    def delete_all_volumes(conn):
        """ Deletes all volumes """

        # Loop through volumes and delete them all
        for vol in conn.get_all_volumes():
            print vol.id, vol.status
            try:
                vol.delete()
                print vol.id, "Terminated"

            # If a volume deletion raises an exception, notify the user for him to double check
            except exception.EC2ResponseError:
                print "Exception raised: Redirecting to Amazon"
