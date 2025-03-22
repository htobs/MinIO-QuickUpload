# MinIO QuickUpload

**MinIO QuickUpload** 是一个便捷的工具，允许用户通过鼠标右键菜单将文件快速上传到 MinIO 云存储。只需右键点击文件，选择“上传到 MinIO”，文件就会自动上传到配置的 MinIO 存储桶中。

------

## 功能特点

- **一键上传**：通过右键菜单快速上传文件到 MinIO。
- **自动初始化**：首次运行时会自动初始化，包括修改注册表和移动程序文件。
- **配置简单**：通过 `initialize.ini` 文件配置 MinIO 连接信息。

------

## 使用步骤

### 1. 下载项目

从 GitHub 仓库下载项目代码或发布的可执行文件。

### 2. 配置 MinIO 信息

在项目根目录下找到 `initialize.ini` 文件，填写你的 MinIO 配置信息：

```
[MinIO]
endpoint = 你的MinIO连接地址，例如192.168.79.128:9000
access_key = 你的access-key
secret_key = 你的secret-key
bucket_name = 存储桶名称
secure = False  # 默认为False，如果使用 HTTPS，请设置为 True
```

### 3. 运行主程序

双击运行 `main.exe`，程序会自动完成以下操作：

- 将程序文件移动到当前用户的 Home 目录下的 `QuickUpload` 文件夹中。
- 修改注册表，添加右键菜单项“上传到 MinIO”。

### 4. 使用右键上传

右键点击任意文件，选择“上传到 MinIO”，文件将自动上传到配置的 MinIO 存储桶中。

------

## 项目结构

```
MinIO-QuickUpload/
├── main.py                # 主程序脚本
├── Bucket.py			  # MinIO连接工具类
├── tool.py				  # 工具包
├── main.exe               # 打包后的可执行文件
├── initialize.ini         # MinIO 配置文件
├── README.md              # 项目说明文档
└── requirements.txt       # Python 依赖库
├── remove.reg			  # 一键删除注册表
```

安装依赖库：

```
pip install -r requirements.txt
```

------

## 打包为可执行文件

如果你想将项目打包为可执行文件（`main.exe`），可以使用 `PyInstaller`：

```
pyinstaller --onefile --windowed main.py
```

打包后的可执行文件会生成在 `dist` 目录中。

------

## 注意事项

1. **管理员权限**：

   - 首次运行时需要管理员权限，以便修改注册表。
   - 如果运行失败，请尝试右键点击程序，选择“以管理员身份运行”。

2. **配置文件**：

   - 确保 `initialize.ini` 文件中的 MinIO 配置信息正确无误。
   - 如果配置信息有误，上传功能将无法正常工作。

3. **恢复默认**：

   - 如果需要删除右键菜单项，可以创建后缀为.reg的文件，将以下文件输入进去后双击文件即可删除

     ```sh
     Windows Registry Editor Version 5.00
     
     [-HKEY_CLASSES_ROOT\*\shell\MinIOQuickUpload]
     ```

------

## 开源协议

本项目采用 **MIT 开源协议**。详情请参阅 [LICENSE](https://license/) 文件。

------

## 贡献与反馈

欢迎提交 Issue 或 Pull Request 来改进本项目！如果你有任何问题或建议，请通过以下方式联系我：

- **Email**: 669059163@qq.com
- **Blog**: http://www.perlink.cc/

------

## 致谢

感谢 MinIO 提供的强大云存储服务，以及开源社区的支持！