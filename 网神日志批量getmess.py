import xlrd
import xlwt
import re
import os


def re_handle(cmpstr, str):
    result = re.match(cmpstr, str)
    if result:
        result = result.group(1)
        return result
    else:
        print("正则出错")
        return


# filepath
file_dir = input("请输入docx文件的路径")
par_file_dir = file_dir + "\\..\\"
os.chdir(par_file_dir)

# config
re_user = ["[\s\S]*[\"]{0,1}username[\"]{0,1}:[\"](.+?)[\"][\s\S]*", "[\s\S]*[&]username=([\s\S]{1,12})[&][\s\S]*",
           "[\s\S]*[&]user=([\s\S]{1,12})[&][\s\S]*", "[\s\S]*[&]usr=([\s\S]{1,12})[\s\S]*", "[\s\S]*[\"]{0,1}user[\"]{0,1}:[\"]([\s\S]{1,12})[\"][\s\S]*"
           ]
re_password = ["[\s\S]*[\"]{0,1}password[\"]{0,1}:[\"](.+?)[\"]{1}[\s\S]*", "[\s\S]*[&]password=([\s\S]{1,12})[&]{1}[\s\S]*",
           "[\s\S]*[&]pwd=([\s\S]{1,12})[&][\s\S]*", "[\s\S]*[&]pass=(.+?)[\s\S]*", "[\s\S]*[\"]{0,1}pass[\"]{0,1}:[\"](.+?)[\"][\s\S]*","[\s\S]*[\"]{0,1}pwd[\"]{0,1}:[\"](.+?)[\"][\s\S]*"
           ]
username_ls = []
password_ls = []

# 读取的xlsx
workbook = xlrd.open_workbook(file_dir)
worksheet = workbook.sheet_by_index(0)
nrows = worksheet.nrows
ncols = worksheet.ncols

# 写入的xlsx
wb = xlwt.Workbook(encoding="utf-8", style_compression=0)
wb1 = wb.add_sheet('结果整理.xls',cell_overwrite_ok=True)


def get_value(request_value):
    username = 0
    password = 0
    for j in re_user:
        if re.match(j, request_value):
            try:
                username = re_handle(j, request_value)
            except:
                print("获取值出错")
            break
    for j in re_password:
        if re.match(j, request_value):
            try:
                password = re_handle(j, request_value)
            except:
                print("获取值出错")
            break
    return username, password

    # 网神的xls表格格式


def read_xls(worksheet):
    print("获取到表格共 %s行，%s列" % (nrows, ncols))
    for i in range(0, nrows):
        row_value = worksheet.row_values(i)
        request_value = row_value[18]  # 弱密码的在19列
        username, password = get_value(request_value)
        if username != 0:
            username_ls.append(username)
        if password != 0:
            password_ls.append(password)


def write_xls(wb):
    for i in range(len(username_ls)):
        wb.write(1 + i, 0, username_ls[i])
    for j in range(len(password_ls)):
        wb.write(1 + j, 1, password_ls[j])


if __name__ == "__main__":
    read_xls(worksheet)
    username_ls = list(set(username_ls))
    password_ls = list(set(password_ls))
    write_xls(wb1)
    wb.save("result.xls")
