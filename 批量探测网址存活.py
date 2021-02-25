from gevent import monkey
import gevent
from gevent.pool import Pool
monkey.patch_all()  # 保证放在上面
import requests
import os
import shutil
import time


# config
ls_200 = []
ls_300 = []
ls_400 = []
timoutls = []
requests.packages.urllib3.disable_warnings()

def detect(url):
        try:
            r = requests.get(url,timeout = 5 ,verify = False)
            code = r.status_code
            if code == 200:
                ls_200.append(url)
            elif code == 302 or code == 301:
                ls_300.append(url)
            elif str(code)[0] == '4':
                ls_400.append(url)
        except Exception as e:
            timoutls.append(url)
            return


def read_file(file):
    ls = []
    with open(file,"r")as f:
        for i in f:
            value = i.replace("\n","")
            ls.append(value)
        return ls


def make_dir():
    try:
        os.mkdir("result")
        print("文件将输出在result文件夹")
    except:
        print("文件已创建")
        shutil.rmtree('result', ignore_errors=True)
        os.mkdir("result")


def write_data(ls,filename):
    with open(filename,"w")as f:
        for i in ls:
            f.write(i)
            f.write("\n")


if __name__ == "__main__":
    url_file = input(r"请输入url文件的路径")
    url_path = url_file + "\\..\\"
    print(url_path)
    os.chdir(url_path)
    make_dir()
    # 获取url
    urls = read_file(url_file)
    start = time.time()
    # 设置协程数
    p = Pool(20)
    task_ls = []
    for url in urls:
        task_ls.append(p.spawn(detect,url))
    gevent.joinall(task_ls)
    # 计算耗时
    end = time.time()
    cost = end-start
    # 写入url文件
    write_data(ls_200,"result/200.txt")
    write_data(ls_300,"result/300.txt")
    write_data(ls_400, "result/400.txt")
    write_data(timoutls,"result/timeout.txt")
    print("耗时：%.2f"%cost)
