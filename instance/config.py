import os

SECRET_KEY = os.urandom(32).hex().upper()

# 数据库配置
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:root@localhost/test"  # 这个仅用于测试
SQLALCHEMY_BINDS = {
    "realmd": "mysql+mysqlconnector://root:root@localhost/classicrealmd",
    "characters": "mysql+mysqlconnector://root:root@localhost/classiccharacters",
    "cmangos": "mysql+mysqlconnector://root:root@localhost/classicmangos",  # 暂时未使用
    "logs": "mysql+mysqlconnector://root:root@localhost/classiclogs",  # 暂时未使用
}

SERVER_VER = "1.12.1(5875)"  # 服务器支持的客户端版本
SERVER_CLIENT_URL = ""  # 对应客户端下载地址
SERVER_LOGON_URL = ""  # 对应登录器地址

# 服务器配置
SERVERS = {
    "db": {
        "name": "db",
        "exe": "mysqld.exe",
        "path": "d:/wow/cm60/60-20250420/mysql5/bin/",
        "args": " --defaults-file=..\..\my.ini  --console",
        "run": False,
    },
    "gate": {
        "name": "gate",
        "exe": "realmd.exe",
        "path": "d:/wow/cm60/60-20250420/",
        "args": "",
        "run": False,
    },
    "core": {
        "name": "core",
        "exe": "mangosd.exe",
        "path": "d:/wow/cm60/60-20250420/",
        "args": "",
        "run": False,
    },
}

# 管理员登录的salt和verifier,请使用auth_tools.py计算
# 需要使用虚拟环境运行：venv\Scripts\python.exe wow\auth_tools.py
ADMIN_S = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
ADMIN_V = "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"

# 验证码设置
CAPTCHA = {
    "width": 130,  # 图片宽度
    "height": 50,  # 图片高度
    "length": 6,  # 验证码长度
    "font_size": 30,  # 字体大小
    "font_path": "",  # 字体路径，默认"c:\\windows\\fonts\\msyh.ttf"
    "line_count": 10,  # 干扰线数量，0表示不加，线宽1~2
    "dot_count": 200,  # 干扰点数量，0表示不加
}
