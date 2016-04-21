
class GlacierVaults:

    def __init__(self):
        """ Empty GlacierInstance Constructor """

    @staticmethod
    def list_vaults(conn):
        """ Find all Glacier Vaults Instances """

        # Get all vaults associated with this AWS account
        vaults = conn.list_vaults()

        return vaults

    @staticmethod
    def create_vault(conn, name):
        """ Method to create a Glacier Vault with the provided name """

        # Create a vault with a given name
        conn.create_vault(name)

    @staticmethod
    def delete_vault(conn, name):
        """ Method to delete the Glacier Vault with the provided name """

        # Delete a vault with a given name
        conn.delete_vault(name)

    @staticmethod
    def terminate_all_vaults(conn):
        """ Auxiliary method to terminate all the Glacier Vaults """

        # Retrieve all the vaults
        vaults = GlacierVaults.list_vaults(conn)

        # Delete them one by one
        for vault in vaults:
            vault.delete()
