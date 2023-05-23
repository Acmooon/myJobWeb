# coding=UTF-8
import time
from flask import Flask  # 导入Flask模块
from flask import render_template  # 导入模板函数
from flask import request
from flask_sqlalchemy import SQLAlchemy  # 用于连接数据库
from servers import config  # 导入配置文件
from servers import getData
from servers import analyzeData
import _thread

# 创建一个Flask对象（初始化），name代表这个模块的名字
app = Flask(__name__)

# 配置自动加载模板文件（热更新html文件）
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.config.from_object(config)  # 导入配置文件
db = SQLAlchemy(app)  # 获取参数配置，将和数据库相关的配置加载到sqlalchemy对象中

jobName = 'java'
areaName = '中国'
# try:
#     _thread.start_new_thread(getData.main, (jobName, areaName, 1))
#     _thread.start_new_thread(getData.main, (jobName, areaName, 16))
#     _thread.start_new_thread(getData.main, (jobName, areaName, 31))
#     _thread.start_new_thread(getData.main, (jobName, areaName, 46))
# except Exception as e:
#     print('无法启动多线程：',e)
#     getData.main(jobName, areaName, 1)

# 路由
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/index')
def home():
    # 分别对数据库中的数据进行计数
    jobNum = db.session.execute("select count(*) from job_data")
    jobNum = list(jobNum)[0][0]
    comNum = db.session.execute("select count(*) from company_data")
    comNum = list(comNum)[0][0]
    areaNum = db.session.execute("select count(*) from work_area")
    areaNum = list(areaNum)[0][0]
    datas = []
    datas.append(jobNum)
    datas.append(comNum)
    datas.append(areaNum)
    return render_template("index.html",datas=datas)

@app.route('/search')
def search():
    return render_template("search.html")

@app.route('/list',methods=['GET','POST'])
def job_list():
    db.drop_all()
    db.create_all()
    if request.method=='POST':
        global jobName
        jobName = request.form.get('inputJobName')
        global areaName
        areaName = request.form.get('inputAreaName')
        try:
            _thread.start_new_thread(getData.main, (jobName, areaName, 1))
            _thread.start_new_thread(getData.main, (jobName, areaName, 16))
            _thread.start_new_thread(getData.main, (jobName, areaName, 31))
            _thread.start_new_thread(getData.main, (jobName, areaName, 46))
            time.sleep(5)
        except Exception as e:
            print('无法启动多线程：', e)
            getData.main(jobName, areaName, 1)
            time.sleep(5)
    data = db.session.execute("select * from job_data jd, work_area wa where jd.area_id=wa.area_id")
    data = list(data)
    return render_template("list.html",jobDatas=data)

@app.route('/chart')
def chart():
    datas = []
    datas.append(analyzeData.ana_salary())
    datas.append(analyzeData.ana_area(areaName))
    datas.append(analyzeData.ana_edu())
    datas.append(analyzeData.ana_experience())
    datas.append(jobName)
    datas.append(areaName)
    return render_template("chart.html", datas=datas)

@app.route('/wordcloud')
def wordcloud():
    datas = []
    datas.append(analyzeData.ana_jobTitle())
    datas.append(analyzeData.ana_comAttr())
    return render_template('wordcloud.html',datas=datas)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
