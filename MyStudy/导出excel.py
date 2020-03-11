# -*- coding: utf-8 -*-
# -*- author: 任士梅-*-
import xlwt
import pymysql


def export_excel(table_name):
    #连接数据库 查询数据
    host,user,password,db='127.0.0.1','root','root','drftest'
    conn = pymysql.connect(user=user,host=host,port=3306,password=password,db=db,charset='utf8')
    cur = conn.cursor()
    sql = "select*from %s"%table_name
    cur.execute(sql)  #返回受影响的行数
    fields = [field[0] for field in cur.description]  #获取所有字段名

    all_data = cur.fetchall()  #所有数据

    #写入到Excel
    wb = xlwt.Workbook()
    #添加一个表
    ws = wb.add_sheet("student")

    for col,field in enumerate(fields):
        ws.write(0,col,field)
    row = 1
    for data in all_data:
        for col,field in enumerate(data):
            ws.write(row, col, field)
        row +=1
    wb.save("%s.xls"%table_name)


if __name__ == '__main__':
    export_excel('tb_student')




