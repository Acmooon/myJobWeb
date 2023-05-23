# coding=UTF-8
# 连接数据库相关变量
HOST = 'localhost' # 主机地址 127.0.0.1
PORT = '3306'      # mysql端口号
USERNAME = 'root'  # mysql数据库用户名
PASSWORD = 'hzr1227001108' #对应密码
DATEBASE = 'jobweb2'  # 使用数据库名称
# python 数据库连接url-编码使用utf8mb4
DB_URL = 'mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8mb4'\
    .format(username=USERNAME,password=PASSWORD,host=HOST,port=PORT,db=DATEBASE)

# print(DB_URL)
SQLALCHEMY_DATABASE_URI = DB_URL  # 数据库连接url
SQLALCHEMY_TRACE_MODIFICATIONS = False

# flask-sqlacodegen 'mysql+pymysql://root:hzr1227001108@localhost:3306/jobweb2?charset=utf8mb4' --outfile "models.py"  --flask


