# coding=UTF-8
# 导入配置文件
from . import config
import pymysql # 用于操作数据库
import threading # 用于操作线程

# 数据库连接相关变量
host = config.HOST
port = config.PORT
username = config.USERNAME
password = config.PASSWORD
database = config.DATEBASE

# 使用pymysql连接数据库
db = pymysql.connect(
    host=host,
    port=3306,
    user=username,
    password=password,
    db=database,
    charset='utf8'
)
# 使用cursor()方法获取数据库的操作游标
# 获取游标的目的就是要执行sql语句，完成对数据库的增删改查
cursor = db.cursor()
# cursor的execute()方法执行sql语句（字符串）
# 执行后使用db的commit()方法提交
# db.rollback() 数据库回滚（撤销刚刚所做的sql语言，将数据库状态返回至操作之前
# cursor的fetchall()方法获取查询后的所有数据（元组）
# cursor的fetchone()方法获取查询后的一条数据（元组）
# cursor.close() 关闭游标
# db.close() 关闭数据库连接

tlock = threading.Lock()
# tlock.acquire() 加锁
# tlock.release() 解锁


# 根据城市名字获取城市id
def get_cityId(city):
    try:
        tlock.acquire() # 加锁
        sql = 'select area_id from work_area where area_name="{}"'.format(city)
        print("sql = ",sql)
        cursor.execute(sql) # 执行sql语句
        city_id = cursor.fetchone() # 获取查询到的数据
        db.commit()
        tlock.release() # 解锁
        print("city_id = ",city_id)
        # 若未查询到，则放回'000000'
        if city_id == None:
            return '000000'
        else:
            return city_id[0]
    except Exception as e:
        print('查询失败：',e)
        return 0
# 将数据写入数据库（插入数据，表）
def write_db(data,table):
    try:
        tlock.acquire()
        if table == 0: # 向job_data插入
            sql0='insert into job_data' \
                 '(job_id,job_href,company_id,job_title,area_id,job_salary,salary_min,' \
                 'salary_max,job_welf,job_education,job_experience,job_update)' \
                 'value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            rows = cursor.execute(sql0,data)
        elif table == 1: # 向company_data插入
            sql1='insert into company_data' \
                 '(company_id,company_href,company_name,company_type,company_attribute,company_size)' \
                 'value (%s,%s,%s,%s,%s,%s)'
            rows = cursor.execute(sql1,data)
        elif table == 2: # 向work_area表插入
            sql2='insert into work_area' \
                 '(area_id,area_name,parent_id)' \
                 'value (%s,%s,%s)'
            rows = cursor.execute(sql2,data)
        db.commit()
        tlock.release()
        print(get_table(table)+'数据插入成功')
        return 1
    except Exception as e:
        db.rollback()
        tlock.release()
        print(get_table(table)+'数据插入失败:',e)
        return 0

# 清空数据库数据（每次爬虫前清空，保证数据时效性）
def data_clr(table):
    tableName = get_table(table)
    if table==2:
        print(tableName+'禁止清空')
        return
    try:
        tlock.acquire()
        cursor.execute("delete from "+tableName)
        db.commit()
        tlock.release()
        print(tableName+'表已清空')
    except Exception as e:
        print(tableName+'表清空失败:',e)

def get_table(table):
    if table == 0:
        return 'job_data'
    elif table ==1:
        return 'company_data'
    elif table ==2:
        return 'work_area'
    else:
        return 'this table is not exist'

# if __name__=="__main__":
#     cityId = get_cityId('杭州')
#     print(cityId)







