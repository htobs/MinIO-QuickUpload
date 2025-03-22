import configparser
import os
import shutil
import winreg
import win32api, win32con


def show_error_message(message: str):
    """
    错误信息框
    :param message: 信息内容
    :return:
    """
    win32api.MessageBox(0, message, "错误", win32con.MB_ICONERROR)


def show_success_message(message: str):
    """
    成功信息框
    :param message: 信息内容
    :return:
    """
    win32api.MessageBox(0, message, "成功", win32con.MB_ICONINFORMATION)


def read_config(file_path: str):
    """
    读取配置文件内容
    :return:
    """
    config = configparser.ConfigParser()
    config.read(file_path)
    if 'MinIO' not in config:
        show_error_message("配置文件中没有找到 [MinIO] 部分")
        return None
    return config['MinIO']


def create_upload_minio_dir():
    """
    在用户文件夹下创建QuickUpload文件夹
    :return:
    """
    target_dir = os.path.join(os.path.expanduser("~"), "QuickUpload")
    os.makedirs(target_dir, exist_ok=True)
    return target_dir


def move_self_to_upload_minio(target_dir: str, current_script_path: str):
    """
    将当前脚本移动到QuickUpload文件夹
    :param target_dir:
    :param current_script_path:
    :return:
    """
    script_name = os.path.basename(current_script_path)
    target_script_path = os.path.join(target_dir, script_name)

    if os.path.exists(target_script_path):
        os.remove(target_script_path)

    shutil.move(current_script_path, target_script_path)
    return target_script_path


def add_registry_entry(target_script_path):
    """
    新增注册表项，支持单个文件和多个文件，但不支持文件夹
    :param target_script_path: 脚本的绝对路径
    :return:
    """
    try:
        reg_path_single = r"*\shell\MinIOQuickUpload"  # 单个文件
        reg_path_multi = r"Directory\shell\MinIOQuickUpload"  # 多个文件

        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, reg_path_single)
        winreg.SetValue(key, "", winreg.REG_SZ, "上传到MinIO")
        winreg.CloseKey(key)

        command_path_single = reg_path_single + r"\command"
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, command_path_single)
        winreg.SetValue(key, "", winreg.REG_SZ, f'"{target_script_path}" "%1"')
        winreg.CloseKey(key)

        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, reg_path_multi)
        winreg.SetValue(key, "", winreg.REG_SZ, "上传到MinIO")
        winreg.CloseKey(key)

        command_path_multi = reg_path_multi + r"\command"
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, command_path_multi)
        winreg.SetValue(key, "", winreg.REG_SZ, f'"{target_script_path}" "%1"')
        winreg.CloseKey(key)
    except Exception as e:
        show_error_message(f"添加注册表项时出错：{e}")


def check_registry_entry():
    """
    检查注册表项是否存在
    :return: True 如果注册表项存在，否则返回 False
    """
    try:
        reg_path_single = r"*\shell\MinIOQuickUpload"  # 单个文件
        reg_path_multi = r"Directory\shell\MinIOQuickUpload"  # 多个文件
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, reg_path_single)
        winreg.CloseKey(key)
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, reg_path_multi)
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"检查注册表项时出错：{e}")
        return False
