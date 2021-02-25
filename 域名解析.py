import subprocess
import xlwt
import os
import re


wb = xlwt.Workbook(encoding="utf-8", style_compression=0)
wb1 = wb.add_sheet('域名解析结果')
re_ip = "[\s\S]* (\d{2,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3})[\s\S]*"
ls_result = []
ls_domain = []

def re_handle(cmpstr, str):
    result = re.match(cmpstr, str)
    if result:
        result = result.group(1)
        return result
    else:
        print("正则出错")
        return


def get_nslookup(domain):
    # resp = subprocess.Popen("nslookup {0}".format(domain), stdin=subprocess.PIPE,
    #                        stdout=subprocess.PIPE).communicate()[0]
    # bs = str(resp,encoding="utf-8")
    ret = os.popen("nslookup {0}".format(domain))
    content = ret.read()
    result = re_handle(re_ip,content)
    if result == "10.118.5.10":
        result = "域名不存在"
    ls_result.append(result)
    print(result)



with open("domain.txt","r")as f:
    for i in f:
        domain = i .replace("\n","")
        ls_domain.append(i)
        get_nslookup(domain)


wb1.write(0,0,"域名")
wb1.write(0,1,"IP")
for i in range(0,len(ls_domain)):
    wb1.write(1+i,0,ls_domain[i])
    wb1.write(1+i,1,ls_result[i])
wb.save("result.xls")
# get_nslookup("cloud.uniin.cn")
print(ls_result)
print("查询的域名数:",len(ls_domain))
print("查询的结果数:",len(ls_result))
