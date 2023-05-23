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

