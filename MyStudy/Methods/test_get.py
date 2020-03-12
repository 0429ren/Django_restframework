# -*- coding: utf-8 -*-
# -*- author: 任士梅-*-

# result = [
#     {'user_id':123456, 'name':'天空蓝', 'subject':'数学'}
# ]
import pymysql
import xlwt


#连接数据库
def get_db_conn(DBS):
    return pymysql.connect(user=DBS['user'],host=DBS['host'],port=DBS['port'],password=DBS['password'],db=DBS['database'],charset=DBS['charset'])

#创建数据库连接对象并执行sql
def get_db_curser(con,sql):
    cur = con.cursor()
    cur.execute(sql)
    count = cur.execute(sql)
    data = cur.fetchall()
    fields = [field[0] for field in cur.description]  # 获取所有字段名
    return count,data,fields

#对获取的数据进行处理 处理成json格式 便于调用返回给客户端
def get_data_result(count,data):
    student_data ={}
    student_list = []
    student_data['total_count'] = count
    student_data['student_list'] = student_list
    for dat in data:
        data_dict = {}
        data_dict['id'] = dat[0]
        data_dict['name'] = dat[1]
        data_dict['sex'] = dat[2]
        data_dict['age'] = dat[3]
        data_dict['class_null'] = dat[4]
        data_dict['description'] = dat[5]
        student_list.append(data_dict)
    return student_data,student_list

#将数据导出到excel
def export_data_to_excel(tb_name,student_all_data,fields):
    # 写入到Excel
    wb = xlwt.Workbook()
    # 添加一个表
    ws = wb.add_sheet("student")

    for col, field in enumerate(fields):
        ws.write(0, col, field)
    row = 1
    for data in student_all_data:
        for col, field in enumerate(data):
            ws.write(row, col, field)
        row += 1
    wb.save("%s.xls" % tb_name)


# #将数据导出到excel
# def export_data_to_excel(student_list):
#     columns = ['id','name', 'sex', 'age', 'class_null', 'description']
#     columns_ext = {'id': '学生ID', 'name': '姓名', 'sex': '性别', 'class_null': '班级序号','description': '个人介绍'}
#     writer = ExportExcel(columns=columns,data_list=student_list,columns_ext=columns_ext)
#     bio = writer.export()
#     return bio

if __name__ == '__main__':
    DBS = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "root",
        "database": "drftest",
        "charset": "utf8",
        "use_unicode": False,
    }
    conn = get_db_conn(DBS)
    tb_name = input('请输入表名:')
    sql = "select*from %s"%tb_name
    count,data,fields = get_db_curser(conn,sql)
    student_data,student_list=get_data_result(count, data)
    export_data_to_excel(tb_name,data,fields)
    # export_data_to_excel(student_list)
