from selenium import webdriver
from lxml import html
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import random
import re 
# 爬虫破解滑动验证码-https://www.cnblogs.com/moning/p/8318475.html
# 下载chromedriver-https://blog.csdn.net/weixin_41990913/article/details/90936149
# chromedriver安装配置-https://www.bilibili.com/read/cv4354566/
# python3 selenium chromedriver被反爬识别的解决办法-https://blog.csdn.net/wywinstonwy/article/details/104902029
# 解决视频教程-https://www.bilibili.com/video/BV1bT4y1u7FA/?spm_id_from=autoNext
# 命令行执行命令-在chrome安装目录下方打开cmd
# chrome --remote-debugging-port=9222（在执行程序前打开）

def get_job_detail(url):
    regjob = re.compile(r'https://(.*?)51job.com', re.S)
    it = re.findall(regjob, url)
    # 在字符串中找到正则表达式所匹配的所有子串，并返回一个列表
    if it != ['jobs.']: #如果匹配到的字符串中括号部分不为jobs. (我们需要匹配的url形式为https://jobs.51job.com/
        print("it = ",it)
        print('不匹配jobs')
        return
    # 配置chrome_options
    option = webdriver.ChromeOptions()
    option.binary_location = 'C:\Program Files (x86)\Google\Chrome\Application' #chrome安装地址
    option.add_experimental_option('debuggerAddress','127.0.0.1:9222') #测试端口
    driver=webdriver.Chrome(chrome_options=option) #新建一个driver
    # driver=webdriver.Chrome()
    driver.get(url) #打开链接
    time.sleep(0.1) #可以等一下页面加载
    res = html.etree.HTML(driver.page_source) # 获取当前页面的etree元素
    judge = res.xpath('/html/head/title/text()')[0] #获取属性判断是否为验证码界面
    print("judge = ",judge)
    if judge=='滑动验证页面':
        wait=WebDriverWait(driver,0.5)
        # wait的使用-https://blog.csdn.net/g123ggf/article/details/77776113
        distance = 260 + random.random()*100 #滑动distance的距离，random防止被反爬
        print("distance = ",distance)
        try:
            #定位class为nc_bg的元素
            button=wait.until(EC.presence_of_element_located((By.CLASS_NAME,'nc_bg')))
            ActionChains(driver).click_and_hold(button).perform() #按下鼠标
            ActionChains(driver).move_by_offset(xoffset=distance,yoffset=0).perform() #移动distance的距离
            # time.sleep(0.2) 
            ActionChains(driver).release().perform() #松开鼠标
            print("验证成功")
        except Exception as e:
            print("验证失败")
            print(e)
    time.sleep(0.25) 
    # print(driver.page_source)
    # driver.close()
    return driver.page_source #放回job详情页的元素内容

# url = "https://jobs.51job.com/hangzhou-yhq/134386898.html?s=sou_sou_soulb&t=0_0"
# get_job_detail(url)


# # 招聘详情
    # # content = data.xpath('string(/html/body/div[3]/div[2]/div[3]/div[1]/div)') #可以一步执行，直接调用xpath中的string函数
    # contents = data.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div')
    # # print("contents = ",contents," type: ",type(contents))
    # # print("contents[0] = ",contents[0]," type: ",type(contents[0]))
    # content = contents[0].xpath('string(.)') #注:xpath提取出来是一个列表，其中的元素才是节点，进行xpath操作
    # # print("content = ",content)
    # content = "".join(content.split()) #去除空格，先split()再join()
    # # print("content = ",content)





















# def get_data_test(url): 
#     print('get_data_url = ',url)
#     # 初始化etree
#     etree = html.etree
    
#     list_all = []
#     data = request(url)
#     print("data = ",data)
#     # 职位名称
#     titles = data.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/h1/@title')
#     print("titles = ",titles)
#     print("titles[0] = ",titles[0])
#     # 公司
#     company = data.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[1]/a[1]/@title')[0]
#     print("company = ",company)
#     # 标签
#     ltype = data.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/@title')[0]
#     print("ltype = ",ltype)
#     print("ltype.split() = ",ltype.split())
#     ltype_str = "".join(ltype.split())
#     print("ltype_str = ",ltype_str)
#     ltype_list = ltype_str.split('|')
#     print("ltype_list =",ltype_list)
#     # 城市地区
#     address = ltype_list[0]
#     # 经验
#     exper = ltype_list[1]
#     # 学历 & 发布日期
#     if len(ltype_list) >= 5:
#         edu = ltype_list[2]
#         dateT = ltype_list[4]
#     else:
#         edu = "没有要求"
#         dateT = ltype_list[-1] # 列表最后一项为发布日期
#     print("edu = ",edu)
#     print("dateT = ",dateT)

#     # 薪资
#     salary = data.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/strong/text()')
#     print("salary = ",salary)
#     if len(salary) == 0:
#         salary_list = [0, 0]
#     else:
#         salary_list = salary_alter(salary[0])
#     print("salary_list = ",salary_list)

#     # 招聘详情
#     # content = data.xpath('string(/html/body/div[3]/div[2]/div[3]/div[1]/div)') #可以一步执行，直接调用xpath中的string函数
#     contents = data.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div')
#     # print("contents = ",contents," type: ",type(contents))
#     # print("contents[0] = ",contents[0]," type: ",type(contents[0]))
#     content = contents[0].xpath('string(.)') #注:xpath提取出来是一个列表，其中的元素才是节点，进行xpath操作
#     # print("content = ",content)
#     content = "".join(content.split()) #去除空格，先split()再join()
#     # print("content = ",content)

#     list_all.append([titles, company, address, salary_list[0],
#                     salary_list[1], dateT, edu, exper, content])
#     # print("list_all = ",list_all)
#     item = [titles, company, address, salary_list[0],
#         salary_list[1], dateT, edu, exper, content]
#     # print("item = ",item)
#     time.sleep(0.2)
    

# if __name__ == "__main__":
#     # url = 'https://jobs.51job.com/wenzhou/133163777.html?s=sou_sou_soulb&t=0_0'
#     # url = 'https://jobs.51job.com/hangzhou-yhq/134377308.html?s=sou_sou_soulb&t=1_0'
#     url = 'https://jobs.51job.com/hangzhou-xhq/130667331.html?s=sou_sou_soulb&t=0_0'
#     get_data_test(url)

# 执行结果(可以和网页对照着看)
# it =  ['jobs.']
# data =  <Element html at 0x27ea6477100>
# titles =  产品经理实习生
# company =  浙江国技互联信息技术有限公司
# ltype =  温州  |  无需经验  |  大专  |  招1人  |  08-10发布
# ltype.split() =  ['温州', '|', '无需经验', '|', '大专', '|', '招1人', '|', '08-10发布']
# ltype_str =  温州|无需经验|大专|招1人|08-10发布
# ltype_list = ['温州', '无需经验', '大专', '招1人', '08-10发布']
# edu =  大专
# dateT =  08-10发布
# salary =  ['4.5-6千/月']
# salary in alter =  4.5-6千/月
# re_salary in alter =  ['4.5', '6']
# res in alter =  [4500.0, 6000.0]
# salary_list =  [4500.0, 6000.0]
# contents =  [<Element div at 0x27ea6470c40>]  type:  <class 'list'>
# contents[0] =  <Element div at 0x27ea6470c40>  type:  <class 'lxml.etree._Element'>
# content =
#         岗位职责：根据产品规划，协助产品经理设计APP客户端及PC客户端、移动互联网产品的流程、应用、完成产品原型和流程部署。1、协助产品经理完成产品的需求收 
# 集、流程设计，并持续改进用户体验，跟进产品的设计、开发、测试、上线、运营全过程。2、通过梳理用户反馈、市场反响，持续完善和优化已有产品，研发新的产品， 推 
# 出更多产品服务。3、负责协调相关部门，配合产品运营，统筹资源进行产品推广。4、产品部门其他相关工作岗位要求：任职要求：1、如果你，热衷互联网，酷爱智能产品如
# 果你，Axure、Visio、XMind工具玩的都很溜2、如果你，美感敏锐，是个创意奇才如果你，紧跟潮流，掌握潮流前沿3、如果你，集学习力、逻辑力、判断力、抗压力、应变力
# 、沟通能力于一身4、如果你，还是一枚文艺青年那么,还等什么？赶紧加入我们吧！

#                                         职能类别：产品助理

#         微信分享



# content =  岗位职责：根据产品规划，协助产品经理设计APP客户端及PC客户端、移动互联网产品的流程、应用、完成产品原型和流程部署。1、协助产品经理完成产品的需求
# 收集、流程设计，并持续改进用户体验，跟进产品的设计、开发、测试、上线、运营全过程。2、通过梳理用户反馈、市场反响，持续完善和优化已有产品，研发新的产品，推
# 出更多产品服务。3、负责协调相关部门，配合产品运营，统筹资源进行产品推广。4、产品部门其他相关工作岗位要求：任职要求：1、如果你，热衷互联网，酷爱智能产品如
# 果你，Axure、Visio、XMind工具玩的都很溜2、如果你，美感敏锐，是个创意奇才如果你，紧跟潮流，掌握潮流前沿3、如果你，集学习力、逻辑力、判断力、抗压力、应变力
# 、沟通能力于一身4、如果你，还是一枚文艺青年那么,还等什么？赶紧加入我们吧！职能类别：产品助理微信分享
# list_all =  [['产品经理实习生', '浙江国技互联信息技术有限公司', '温州', 4500.0, 6000.0, '08-10发布', '大专', '无需经验', '岗位职责：根据产品规划，协助产
# 品经理设计APP客户端及PC客户端、移动互联网产品的流程、应用、完成产品原型和流程部署。1、协助产品经理完成产品的需求收集、流程设计，并持续改进用户体验，跟进 
# 产品的设计、开发、测试、上线、运营全过程。2、通过梳理用户反馈、市场反响，持续完善和优化已有产品，研发新的产品，推出更多产品服务。3、负责协调相关部门，配 
# 合产品运营，统筹资源进行产品推广。4、产品部门其他相关工作岗位要求：任职要求：1、如果你，热衷互联网，酷爱智能产品如果你，Axure、Visio、XMind工具玩的都很溜
# 2、如果你，美感敏锐，是个创意奇才如果你，紧跟潮流，掌握潮流前沿3、如果你，集学习力、逻辑力、判断力、抗压力、应变力、沟通能力于一身4、如果你，还是一枚文艺
# 青年那么,还等什么？赶紧加入我们吧！职能类别：产品助理微信分享']]
# item =  ['产品经理实习生', '浙江国技互联信息技术有限公司', '温州', 4500.0, 6000.0, '08-10发布', '大专', '无需经验', '岗位职责：根据产品规划，协助产品经理
# 设计APP客户端及PC客户端、移动互联网产品的流程、应用、完成产品原型和流程部署。1、协助产品经理完成产品的需求收集、流程设计，并持续改进用户体验，跟进产品的 
# 设计、开发、测试、上线、运营全过程。2、通过梳理用户反馈、市场反响，持续完善和优化已有产品，研发新的产品，推出更多产品服务。3、负责协调相关部门，配合产品 
# 运营，统筹资源进行产品推广。4、产品部门其他相关工作岗位要求：任职要求：1、如果你，热衷互联网，酷爱智能产品如果你，Axure、Visio、XMind工具玩的都很溜2、如 
# 果你，美感敏锐，是个创意奇才如果你，紧跟潮流，掌握潮流前沿3、如果你，集学习力、逻辑力、判断力、抗压力、应变力、沟通能力于一身4、如果你，还是一枚文艺青年 
# 那么,还等什么？赶紧加入我们吧！职能类别：产品助理微信分享']