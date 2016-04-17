from boto.s3.key import Key


class S3Bucket:
    def __init__(self):
        """ S3Bucket Constructor """

    @staticmethod
    def list_buckets(conn):
        """ List S3 buckets """
        buckets = conn.get_all_buckets()

        return buckets

    @staticmethod
    def create_bucket(conn, bucket_title):
        """ Create a new Bucket """
        bucket = conn.create_bucket(bucket_title)
        return bucket

    @staticmethod
    def delete_bucket(conn, bucket_title):
        """ Delete a new Bucket """
        conn.delete_bucket(bucket_title)

    @staticmethod
    def store_in_bucket(bucket, file_title, file_location):
        """ Store a file inside a Bucket """

        k = Key(bucket)
        # k.key = 'testing.txt'
        # k.set_contents_from_filename('res/text.txt')
        k.key = file_title
        k.set_contents_from_filename(file_location)

    @staticmethod
    def delete_from_bucket(bucket, file_title):
        """ Delete a file from a Bucket """

        return bucket.delete_key(file_title)
