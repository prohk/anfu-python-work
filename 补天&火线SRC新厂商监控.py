import requests
import time
import smtplib
from email.message import EmailMessage

# config
mail_host= "smtp.qq.com"    # 邮箱得开启smtp
mail_user = ""    # 你的邮箱，目前模式是自己发自己
mail_pass = ""     # 授权码
mail_from = mail_user
mail_to = mail_user

def sendmail(content,src_name):
    # login
    smtp = smtplib.SMTP()
    print(smtp.connect(mail_host, 25))
    print(smtp.login(mail_user, mail_pass))
    #sendmail
    msg = EmailMessage()
    msg.set_content(f"{src_name}更新了一个新的厂商：{content}")
    msg['Subject'] = f'{src_name}更新了'
    msg['From'] = mail_from
    msg['To'] = mail_to
    try:
        smtp.send_message(msg)
        print("邮件发送成功")
    except Exception as e:
        print("发送邮件异常:",e)


def get_butian(old_src):
    now_src = []
    headers = {
'Host':'www.butian.net',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Accept':'application/json, text/javascript, */*; q=0.01',
'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
'Accept-Encoding':'gzip, deflate',
'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
'X-Requested-With':'XMLHttpRequest',
'Referer': 'https://www.butian.net/Reward/plan/2',
'Content-Length':'21',
'Cache-Control': 'no-cache'
    }
    # proxy = {
    #     "https": "https://127.0.0.1:8087"
    # }
    resp = requests.post(url="https://www.butian.net/Reward/corps", data="s=3&p=1&sort=1&token=", headers=headers)
    resp_result = resp.json()
    lists = resp_result['data']['list']
    print("已获取到最新的补天SRC专属厂商")

    for i in lists:
        now_src.append(i['company_name'])
    # 判断！如果SRC更新了，发邮件提醒
    # if old_src[0] != now_src[0]:
    #     sendmail(now_src[0],"补天SRC")
    #     print(f"补天更新了:{now_src[0]}")
    # else:
    #     print("补天专属没有发生更新")
    # 加一重判断
    for i in now_src:
        if i not in old_src:
            sendmail(i,"补天SRC")
            print(f"补天更新了:{i}")
    # 判断，如果SRC出现变动，更新src.txt
    if len(lists) != len(old_src):
        write_src_totxt(now_src)
    return now_src


def get_huoxian():
    now_date = time.strftime('%Y-%m-%d')
    headers = {
        'Host': 'www.huoxian.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Length': '24',
        'Cache-Control': 'max-age=0',
        'x - token': ''   #这里填你的火线  x-token
    }
    resp = requests.post(url="https://www.huoxian.cn/fireapi/fireapp/projectList/", data='{"page":1,"page_size":9}', headers=headers)
    resp_result = resp.json()
    value = resp_result['data']['results']
    for i in value:
        the_stamp = i["begintime"]
        result = compare_date(the_stamp,now_date)
        if result ==0:
            name = i["name"]
            content = name + " 预备上线状态中！"
            sendmail(content,"火线SRC")
            return
        elif result ==1:
            name = i["name"]
            content = name + "今天上线！"
            sendmail(content,"火线SRC")
            return
    
    print("火线SRC没有最新的厂商上线")



# 读取txt中的src，返回旧src数组
def read_src():
    old_src = []
    with open("butian.txt","r",encoding='utf-8')as f:
        for i in f:
            company = i.replace("\n","")
            old_src.append(company)
        return old_src

def compare_date(timestamp,now_date):
    now_stamp = time.time()
    if timestamp > now_stamp:
        return 0    # 预备上线情况
    the_date = time.localtime(timestamp)
    the_date = time.strftime('%Y-%m-%d', the_date)
    if the_date == now_date:
        return 1    # 上线年月日相同情况
    else:
        return 2

# 更新旧的SRC.txt
def write_src_totxt(ls):
    with open("butian.txt","w",encoding='utf=8')as g:
        for i in ls:
            g.write(i)
            g.write("\n")



def task_run():
    old_src = read_src()
    get_butian(old_src)
    time.sleep(5)
    try:
        get_huoxian()
    except:
        print("获取火线SRC信息错误")


if __name__ == "__main__":
    # sendmail("test","test")
    while True:
        print("***************补天&&火线SRC.monitor*********************")
        print("********第一次使用请在config下填好邮件信息及火线x-token*********")
        task_run()
        print("休息一小时后再监测")
        time.sleep(3600)




