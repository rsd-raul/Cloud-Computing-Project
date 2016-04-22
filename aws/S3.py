from boto.s3.key import Key


class S3Bucket:
    def __init__(self):
        """ S3Bucket Constructor """

    @staticmethod
    def list_buckets(conn):
        """ List S3 buckets """

        # Get all the buckets for the user
        buckets = conn.get_all_buckets()

        return buckets

    @staticmethod
    def create_bucket(conn, bucket_title):
        """ Create a new Bucket """

        # Create a new bucket with the given title
        bucket = conn.create_bucket(bucket_title)

        return bucket

    @staticmethod
    def delete_bucket(conn, bucket_title):
        """ Delete a new Bucket """

        # Delete the bucket with the given title
        conn.delete_bucket(bucket_title)

    @staticmethod
    def store_in_bucket(bucket, file_title, file_location):
        """ Store a file inside a Bucket """

        try:
            # Create a Key with the title and the content of the location provided
            k = Key(bucket)
            k.key = file_title
            k.set_contents_from_filename(file_location)
            return True

        # Notify the user if the location of the archive does not correspond with one
        except OSError:
            print "The file does not exist"
            return False
        except IOError:
            print "No such file or directory"
            return False

    @staticmethod
    def delete_from_bucket(bucket, file_title):
        """ Delete a file from a Bucket """

        # Delete from the provided bucket using the unique file title
        return bucket.delete_key(file_title)
