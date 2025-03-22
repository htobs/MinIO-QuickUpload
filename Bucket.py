from minio import Minio,S3Error


class Bucket(object):
    """
    MinIO工具类（只包含上传功能）
    """
    client = None

    def __new__(cls, *args, **kwargs):
        if not cls.client:
            cls.client = object.__new__(cls)
        return cls.client

    def __init__(self, endpoint, access_key, secret_key, secure=False):
        self.endpoint = endpoint
        self.client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=secure)

    def exists_bucket(self, bucket_name):
        """
        判断桶是否存在
        :param bucket_name: 桶名称
        :return:
        """
        return self.client.bucket_exists(bucket_name=bucket_name)

    def put_file(self, bucket_name, filename, file_path):
        """
        上传文件
        :param bucket_name: 桶名
        :param filename: 文件名
        :param file_path: 本地文件路径
        :return:
        """
        try:
            print("1"+bucket_name)
            print("2"+filename)
            print("3"+file_path)
            self.client.fput_object(bucket_name, filename, file_path)
        except S3Error as e:
            print("[error]:", e)