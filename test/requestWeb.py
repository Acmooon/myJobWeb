# coding=UTF-8
import requests
import random
from lxml import html

# 随机获取一个请求头（return 字典对象）
def get_user_agent():
    agent = {
        'User-Agent': random.choice(user_agent),
    }
    return agent

def request(url):
    htmls = requests.get(url,headers=get_user_agent())
    # print(type(htmls))
    # print(htmls)
    htmls.encoding = 'gbk'
    # print(htmls.content)

    f = open("requestWeb.html",'wb') #
    f.write(htmls.content)
    f.close()

    # print(type(html.etree.HTML(htmls.text)))
    # print(html.etree.HTML(htmls.text))

    return html.etree.HTML(htmls.text)



# if __name__ == "__main__":
#     url = 'https://jobs.51job.com/hangzhou/134604505.html?s=sou_sou_soulb&t=0_0'
#     request(url)
