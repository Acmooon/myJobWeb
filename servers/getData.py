# coding=UTF-8
import re
import time
from lxml import html
from . import requestWeb as rw
from . import database as db

# 处理薪资字符串-转化为月薪
def salary_alter(salary):
    # salary == "4.5-6千\/月"
    if salary == '': # 如果获取的薪资数据为空，则返回[0,0]
        return [0,0]
    re_salary = re.findall('\d+\.?\d*',salary) # 提取薪资中的数字（包括小数点）
    salary_min = float(re_salary[0]) # str转化为float
    # 按天计算的薪资没有salary_max
    if len(re_salary)<=1 :
        salary_max = float(re_salary[0])
    else :
        # print("re_salary = ",re_salary)
        salary_max = float(re_salary[1])
    wan = lambda x,y : [x*10000,y*10000]
    qian = lambda x,y : [x*1000,y*1000]
    yuan = lambda x,y : [x,y]
    nian = lambda a : [round(a[0]/12,2),round(a[1]/12,2)] # 返回浮点数四舍五入值,保留两位小数
    tian = lambda a : [a[0]*30,a[1]*30]
    if '年' in salary:
        if '万' in salary:
            res = wan(salary_min,salary_max)
        elif '千' in salary:
            res = qian(salary_min,salary_max)
        else:
            res = yuan(salary_min,salary_max)
        res = nian(res)
    elif '月' in salary:
        if '万' in salary:
            res = wan(salary_min,salary_max)
        elif '千' in salary:
            res = qian(salary_min,salary_max)
        else:
            res = yuan(salary_min,salary_max)
    elif '天' in salary:
        if '万' in salary:
            res = wan(salary_min,salary_max)
        elif '千' in salary:
            res = qian(salary_min,salary_max)
        else:
            res = yuan(salary_min,salary_max)
        res = tian(res)
    # print("res in alter = ",res)
    return res

# 获取数据并将其写入数据库
def get_data(url):
    # 爬取数据并获得期望的数据文本
    data = rw.request(url)
    text_list = data.xpath('/html/body/script[2]/text()') # 返回一个list
    text = text_list[0]
    # print('type(text):', type(text))
    # print("text = ", text)

    # 声明JOB数据列表
    jobId_list = []
    jobHref_list = []
    jobTitle_list = []

    jobAreaId_list = []
    jobArea_list = []

    jobSalary_list = []
    salaryMin_list = []
    salaryMax_list = []
    jobWelf_list = []

    jobAttribute = []
    jobDegreefrom = []
    jobEducation_list = []
    jobExperience_list = []
    jobUpdate_list = []
    # 声明company数据列表
    companyId_list = []

    companyHref_list = []
    companyName_list = []
    companyType_list = []
    companyAttribute_list = []
    companySizes_list = []

    #从数据文本中通过正则表达式获得需要的数据

    # 职位Id
    jobId_list = re.findall(r'\"jobid\":"(.*?)"', text)

    # 职位详细页面链接
    jobHref_list = re.findall(r'\"job_href\":"(.*?)"', text)
    for (href, i) in zip(jobHref_list, range(len(jobHref_list))):
        jobHref_list[i] = "".join(href.split("\\"))

    # 职位名称
    jobTitle_list = re.findall(r'\"job_title\":"(.*?)"', text)
    for (title, i) in zip(jobTitle_list, range(len(jobTitle_list))):
        jobTitle_list[i] = "".join(title.split("\\"))

    # 职位工作地点
    jobAreaId_list = re.findall(r'\"workarea\":"(.*?)"', text)
    jobArea_list = re.findall(r'\"workarea_text\":"(.*?)"', text)
    print(len(jobArea_list))

    # 职位薪资
    jobSalary_list = re.findall(r'\"providesalary_text\":"(.*?)"', text)
    for salary in jobSalary_list:
        salaryAlter = salary_alter(salary)  # 处理薪资字符串（形如"4.5-6千\/月"）
        salaryMin_list.append(salaryAlter[0])
        salaryMax_list.append(salaryAlter[1])

    # 职位其他属性
    jobWelf_list = re.findall(r'\"jobwelf\":"(.*?)"', text)

    # 职位所需经验与教育程度 （匹配到的字符串可以见test.json)
    jobDegreefrom = re.findall(r'"degreefrom":"(.*?)"', text)  # 用于判断是否需要学历
    jobAttribute = re.findall(r'"attribute_text":\[(.*?)\]', text)  # 用于获取经验要求与学历要求

    # 从attribute列表中获取学历和经验要求（下标可能会改变）
    eduIndex = 2
    for (attribute, i) in zip(jobAttribute, range(len(jobAttribute))):
        # print("attribute = ",attribute)
        attribute = "".join(attribute.split("\""))  # 去除 "
        attr = attribute.split(",")  # 根据,分割成列表
        # print("attr = ", attr)
        if "经验" in attr[1]:
            jobExperience_list.append(attr[1])
            # print("jobExperience_list = ",jobExperience_list)
            eduIndex = 2
        else:
            jobExperience_list.append("无需经验")
            eduIndex = 1

        if jobDegreefrom[i] != "":
            jobEducation_list.append("".join(attr[eduIndex].split("\\")))
            # print("jobDegreefrom[i] = ",jobDegreefrom[i])
            # print("attr[eduIndex] = ",attr[eduIndex])
        else:
            jobEducation_list.append("无学历要求")
    # print("jobExperience_list = ",jobExperience_list)
    # print("jobEducation_list = ",jobEducation_list)

    # 职位发布日期
    jobUpdate_list = re.findall(r'\"updatedate\":"(.*?)"', text)

    # 工作所属公司Id
    companyId_list = re.findall(r'\"coid\":"(.*?)"', text)

    # 公司链接
    companyHref_list = re.findall(r'\"company_href\":"(.*?)"', text)
    for (href, i) in zip(companyHref_list, range(len(companyHref_list))):
        companyHref_list[i] = "".join(href.split("\\"))  # 去除\

    # 公司名称
    companyName_list = re.findall(r'\"company_name\":"(.*?)"', text)

    # 公司类型
    companyType_list = re.findall(r'\"companytype_text\":"(.*?)"', text)

    # 公司领域
    companyAttribute_list = re.findall(r'\"companyind_text\":"(.*?)"', text)
    for (attribute, i) in zip(companyAttribute_list, range(len(companyAttribute_list))):
        companyAttribute_list[i] = "".join(attribute.split("\\"))  # 去除\

    # 公司规模
    companySizes_list = re.findall(r'\"companysize_text\":"(.*?)"', text)

    # 依次写入数据
    job_list = ['id','href','coid','title','areaid','salary',0,0,'welf','edu','exper','date']
    company_list = ['id','href','name','type','attribute','size']
    area_list = ['id','name','000000']

    for i in range(len(jobId_list)):
        job_list[0] = jobId_list[i]
        job_list[1] = jobHref_list[i]
        job_list[2] = companyId_list[i]
        job_list[3] = jobTitle_list[i]
        job_list[4] = jobAreaId_list[i]
        job_list[5] = jobSalary_list[i]
        job_list[6] = salaryMin_list[i]
        job_list[7] = salaryMax_list[i]
        job_list[8] = jobWelf_list[i]
        job_list[9] = jobEducation_list[i]
        job_list[10] = jobExperience_list[i]
        job_list[11] = jobUpdate_list[i]

        company_list[0] = companyId_list[i]
        company_list[1] = companyHref_list[i]
        company_list[2] = companyName_list[i]
        company_list[3] = companyType_list[i]
        company_list[4] = companyAttribute_list[i]
        company_list[5] = companySizes_list[i]

        area_list[0] = jobAreaId_list[i]
        area_list[1] = jobArea_list[i]
        # 获取parent_id
        # 杭州-萧山区
        addr = re.findall(r'(.*?)-',jobArea_list[i])
        # print(jobArea_list[i])
        # print(addr)
        if addr == []:
            area_list[2]='000000'
        else:
            area_list[2]=db.get_cityId(addr[0])

        # 由于数据库外键，所以需要先插入area和company数据
        global db_item
        db.write_db(area_list,2)
        db.write_db(company_list, 1)
        # 返回插入条数并统计
        db_item += db.write_db(job_list, 0)


# 传入 搜索关键词 城市 起始页码

def main(kw,city,startpage):
    inputData = 0;
    city_id = db.get_cityId(city)


    db.data_clr(0) # 清空job_data数据，保持数据时效性
    db.data_clr(1) # 清空company_data数据
    page = startpage
    global db_item # 表示数据库插入条数
    db_item = 0
    while(db_item<1000):
        print("page = ",page)
        url = "https://search.51job.com/list/{},000000,0000,00,9,99,{},2,{}.html".format(city_id,kw,page)
        get_data(url)
        page += 1
        if page > 65:
            break
        print(db_item)

# if __name__ == "__main__":
#     main('java','合肥',14)
