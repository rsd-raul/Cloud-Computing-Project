from boto import exception


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
            #     print '**********************************'
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

        if volume is None:
            print "No volume with that id"
            return False

        if volume.status != "available":
            print "Volume in use"
            return False

        result = volume.attach(instance_id, '/dev/sdh')

        if result:
            print 'Volume ', volume_id, ' attached successfully to instance', instance_id, '\n'
            return True
        else:
            print 'There`s an error attaching the volume ', volume_id, 'to the instance ', instance_id
            return False

    @staticmethod
    def detach_volume(conn, volume_id):
        """ Detaches a specific volume """

        # Loop through volumes to find the matching one (by id)
        volume = None
        for vol in conn.get_all_volumes():
            if vol.id == volume_id:
                volume = vol

        if volume is None:
            print "No volume with that id"
            return False

        if volume.status != "in-use":
            print "Volume in not attached"
            return False
        try:
            result = volume.detach()
            if result:
                print 'Volume ', volume_id, ' detached successfully\n'
                return True

        except exception.EC2ResponseError:
            print "There's an error detaching the volume", volume_id
            return False

    @staticmethod
    def create_volume(conn):
        """ Creating a new volume """
        try:
            conn.create_volume(30, "eu-west-1c", None, "gp2", None, False, None, False)
            return True
        except exception.EC2ResponseError:
            print "Problems creating volume"
            return False

    @staticmethod
    def delete_all_volumes(conn):
        """ Deletes all volumes """

        # Loop through volumes and detach them all
        for vol in conn.get_all_volumes():
            print vol.id, vol.status
            try:
                vol.delete()
                print vol.id, "Terminated"
            except exception.EC2ResponseError:
                print "Exception raised: Redirecting to Amazon"
