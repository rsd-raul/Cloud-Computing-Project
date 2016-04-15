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
    def store_in_bucket(conn, bucket_title, file_title, file_location):
        """ Store a file inside a Bucket """
        buckets = conn.get_all_buckets()
        for bucket in buckets:
            if bucket.name == bucket_title:
                k = Key(bucket)
                # k.key = 'myfile'
                # k.set_contents_from_filename('test_file.txt')
                k.key = file_title
                k.set_contents_from_filename(file_location)

    @staticmethod
    def list_objects_bucket(conn, bucket_title):
        """ Store a file inside a Bucket """
        buckets = conn.get_all_buckets()
        for bucket in buckets:
            if bucket.name == bucket_title:
                k = Key(bucket)
                # k.key = 'myfile'
                # k.set_contents_from_filename('test_file.txt')
                k.key = file_title
                k.set_contents_from_filename(file_location)
