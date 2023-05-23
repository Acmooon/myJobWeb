# coding=UTF-8
import re

from .database import db,cursor,get_cityId
import pandas as pd
import jieba
# 分析学历
def ana_edu():
    try:
        cursor.execute('select job_education from job_data')
        fetch_edu = cursor.fetchall() # 获取数据库中的数据（元组）
        db.commit()
        # print(fetch_edu)
        print("edu查询成功")
        df_edu = pd.DataFrame(fetch_edu,columns=['edu']) # 将数据库数据转化为pandas库中的DataFrame类型
        # print(type(df_edu))
        # print(df_edu)
        count_edu = df_edu.value_counts() # 对相同数据进行计数（返回pandas库中的Series类型）
        # print(type(count_edu))
        # print(count_edu)
        print("count_edu.iteritems():",count_edu.iteritems())
        count_edu = list(count_edu.iteritems()) #将series类型转为list类型（需要用iteritems获取键和值）
        print("count_edu = ",count_edu)
        res_edu = []
        # 处理count_edu数据并排序
        for row in count_edu:
            print(row)
            res_edu.append([row[0][0], row[1]])
        res_edu.sort(key=res_sort)
        print(res_edu)
        return res_edu
    except Exception as e:
        print('edu分析失败：',e)
# 分析工作经历
def ana_experience():
    try:
        cursor.execute('select job_experience from job_data')
        fetch_exper = cursor.fetchall()
        db.commit()
        # print(fetch_exper)
        print("exper查询成功")
        df_exper = pd.DataFrame(fetch_exper,columns=['exper'])
        # print(type(df_exper))
        # print(df_exper)
        count_exper = df_exper.value_counts()
        # print(type(count_exper))
        # print(count_exper)
        print("count_exper.iteritems():",count_exper.iteritems())
        count_exper = list(count_exper.iteritems())
        print("count_exper = ",count_exper)
        res_exper = []
        for row in count_exper:
            print(row)
            exper_min = re.findall(r'([0-9]+)', row[0][0])
            if exper_min == []:
                exper_min = ['无需经验']
            print(exper_min)
            res_exper.append([exper_min[0],row[1]])
        res_exper.sort()
        print(res_exper)
        return res_exper
    except Exception as e:
        print('exper分析失败：',e)
# 分析薪资
def ana_salary():
    try:
        cursor.execute('select salary_min,salary_max from job_data')
        fetch_salary = cursor.fetchall()
        db.commit()
        print('salary查询成功')
        print(fetch_salary)
        aver_salary = []
        for row in fetch_salary:
            aver_salary.append( (row[0]+row[1])/2 )
        print(aver_salary)
        # 对数据进行分组
        group_salary = pd.cut(aver_salary,[0,100,5000,8000,11000,14000,17000,20000,23000,99999999],right=True)
        print(group_salary)
        count_salary = group_salary.value_counts()
        print(count_salary)
        res_salary = [
            ['暂未发布', count_salary[0] ],
            ['小于5k',   count_salary[1] ],
            ['5k~8k',    count_salary[2] ],
            ['8k~11k',   count_salary[3] ],
            ['11k~14k',  count_salary[4] ],
            ['14k~17k',  count_salary[5] ],
            ['17k~20k',  count_salary[6] ],
            ['20k~23k',  count_salary[7] ],
            ['23k以上',  count_salary[8] ]
        ]
        print(res_salary)
        return res_salary
    except Exception as e:
        print('salary分析失败：',e)
# 分析地区
def ana_area(pArea):
    pId = get_cityId(pArea)
    try:
        # 要求area_id 或者 parent_id 为查询查询城市的id
        cursor.execute("select area_name "
                       "from job_data j,work_area w "
                       "where j.area_id=w.area_id and (w.parent_id='"+pId+"'or w.area_id='"+pId+"')")
        fetch_area = cursor.fetchall()
        db.commit()
        print(fetch_area)
        print("area查询成功")
        df_area = pd.DataFrame(fetch_area, columns=['area'])
        # print(type(df_area))
        # print(df_area)
        count_area = df_area.value_counts()
        # print(type(count_area))
        # print(count_area)
        print("count_area.iteritems():", count_area.iteritems())
        count_area = list(count_area.iteritems())
        print("count_area = ", count_area)
        res_area = [['其他',0]]
        for row in count_area:
            print(row)
            # 如果区域职位数太少，加到"其他"区域中
            if row[1]>=20:
                res_area.append([row[0][0], row[1]])
            else:
                res_area[0][1] += row[1]
        res_area.sort()
        print(res_area)
        return res_area
    except Exception as e:
        print('area分析失败：',e)
# 分析职位名称
def ana_jobTitle():
    try:
        cursor.execute('select job_title from job_data')
        fetch_jobTitle = cursor.fetchall()
        db.commit()
        # print(fetch_jobTitle)
        print("jobTitle查询成功")
        cut_jobTitle = []
        # 使用jieba库进行分词
        for row in fetch_jobTitle:
            cut_jobTitle += list(jieba.cut(row[0]))
        print(cut_jobTitle)
        df_jobTitle = pd.DataFrame(cut_jobTitle,columns=['cutJobTitle'])
        # print(type(df_jobTitle))
        # print(df_jobTitle)
        count_jobTitle = df_jobTitle.value_counts()
        # print(type(count_jobTitle))
        # print(count_jobTitle)
        # print("count_jobTitle.iteritems():",count_jobTitle.iteritems())
        count_jobTitle = list(count_jobTitle.iteritems())
        # print("count_jobTitle = ",count_jobTitle)
        res_jobTitle = []
        for row in count_jobTitle:
            # print(row)
            # 过滤单个字符和数量小于3的词
            if len(row[0][0])>1 and row[1]>3:
                res_jobTitle.append([row[0][0], row[1]])
        print(res_jobTitle)
        return res_jobTitle
    except Exception as e:
        print('jobTitle分析失败：',e)
# 分析公司发展领域
def ana_comAttr():
    try:
        cursor.execute('select company_attribute from job_data j,company_data co where j.company_id=co.company_id')
        fetch_comAttr = cursor.fetchall()
        db.commit()
        # print(fetch_comAttr)
        print("comAttr查询成功")
        cut_comAttr = []
        for row in fetch_comAttr:
            cut_comAttr += list(jieba.cut(row[0]))
        print(cut_comAttr)
        df_comAttr = pd.DataFrame(cut_comAttr,columns=['cutcomAttr'])
        # print(type(df_comAttr))
        # print(df_comAttr)
        count_comAttr = df_comAttr.value_counts()
        # print(type(count_comAttr))
        # print(count_comAttr)
        # print("count_comAttr.iteritems():",count_comAttr.iteritems())
        count_comAttr = list(count_comAttr.iteritems())
        # print("count_comAttr = ",count_comAttr)
        res_comAttr = []
        for row in count_comAttr:
            # print(row)
            if len(row[0][0])>1 and row[1]>3:
                res_comAttr.append([row[0][0], row[1]])
        print(res_comAttr)
        return res_comAttr
    except Exception as e:
        print('comAttr分析失败：',e)


def res_sort(element):
    if element[0] == '无学历要求':
        return '0'
    if element[0] == '小学':
        return '1'
    if element[0] == '中学':
        return '2'
    if element[0] == '中专':
        return '3'
    if element[0] == '高中':
        return '4'
    if element[0] == '大专':
        return '5'
    if element[0] == '在校生/应届生':
        return '6'
    if element[0] == '本科':
        return '7'
    if element[0] == '硕士':
        return '8'
    if element[0] == '博士':
        return '9'


# if __name__=='__main__':
#     ana_jobTitle()

