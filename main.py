import sys
from minio import S3Error
import os
import tool
from Bucket import Bucket


def initialize():
    """
    项目初始化
    1、新增鼠标右键菜单
    2、配置minio
    :return:
    """
    tool.show_success_message("项目即将初始化！")
    if not os.path.exists("initialize.ini"):
        tool.show_error_message("不存在initialize.ini配置文件")
        return
    while True:
        # 连接测试
        try:
            config = tool.read_config("initialize.ini")
            client = Bucket(
                endpoint=config.get("endpoint", "未设置"),
                access_key=config.get("access_key", "未设置"),
                secret_key=config.get("secret_key", "未设置"),
                secure=eval(config.get("secure", "未设置"))
            ).exists_bucket(config.get("bucket_name", "未设置"))
            if client is True:
                break
            tool.show_error_message(f"不存在为{config.get('bucket_name', '未设置')}的存储桶")
            return
        except S3Error as e:
            tool.show_error_message("S3Error: " + str(e.message))
            return
    # 创建文件夹并移动
    if not os.path.exists("initialize.ini"):
        tool.show_error_message("不存在initialize.ini配置文件")
    else:
        target_dir = tool.create_upload_minio_dir()
        tool.move_self_to_upload_minio(target_dir, "initialize.ini")
        target_script_path = tool.move_self_to_upload_minio(target_dir, os.path.abspath(sys.argv[0]))
        tool.add_registry_entry(target_script_path)
        tool.show_success_message("初始化成功！")


def upload(file_path):
    """
    上传文件
    :param file_path:
    :return:
    """
    try:
        target_dir = tool.create_upload_minio_dir()
        config = tool.read_config(os.path.join(target_dir, "initialize.ini"))
        object_name = os.path.basename(file_path)
        client = Bucket(
            endpoint=config.get("endpoint", "未设置"),
            access_key=config.get("access_key", "未设置"),
            secret_key=config.get("secret_key", "未设置"),
            secure=False
        )
        print(config.get("bucket_name", "未设置"))
        client.put_file(bucket_name=config.get("bucket_name", "未设置"), filename=object_name, file_path=file_path)
        tool.show_success_message("文件上传成功")
    except Exception as e:
        tool.show_error_message(str(e))


if __name__ == "__main__":
    # 模拟
    # sys.argv = ["main.py", r"C:\Users\heitu\PycharmProjects\MinIO-QuickUpload-main\requirements.txt"]

    if tool.check_registry_entry() is False:
        initialize()
    else:
        if len(sys.argv) < 2:
            tool.show_error_message("错误：请提供文件路径。")
            sys.exit(1)
        file_path = sys.argv[1].encode('utf-8').decode('utf-8')
        if os.path.exists(file_path):
            upload(file_path)
        else:
            tool.show_error_message("错误：文件路径无效或文件不存在。")
