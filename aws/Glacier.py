
class GlacierVaults:

    def __init__(self):
        """ Empty GlacierInstance Constructor """

    @staticmethod
    def list_vaults(conn):
        """ Find EC2 Instances """

        # Get all instance reservations associated with this AWS account
        vaults = conn.list_vaults()

        return vaults

    @staticmethod
    def create_vault(conn, name):
        """ Find EC2 Instances """

        conn.create_vault(name)

    @staticmethod
    def delete_vault(conn, name):

        conn.delete_vault(name)
