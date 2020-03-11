# -*- coding: utf-8 -*-
# -*- author: 任士梅-*-

import xlwt
from io import BytesIO

class ExportExcel:
    def __init__(self,columns,data_list,columns_ext={},fill_none=""):
        """
        输出excel
        :param columns: 从数据库中表的列名[col1,col2]
        :param data_list: 数据库中表的内容 [{col1:v,col2:v},{col1:v,col2:v},.....]
        :param columns_ext: 数据库表中对应的字段导出到excel的中表时自定义列名 {col1:newname,col2:newname}
        :param fill_none:匹配空值
        """
        self.columns = columns
        self.data_list = data_list
        self.columns_ext = columns_ext
        self.fill_none = fill_none

    def export(self):
        wb = xlwt.Workbook()  #
        wb.encoding = "utf8"
        ws = wb.add_sheet('1') # 设置表名
        #写入表头
        for index,col in enumerate(self.columns):
            col_ext = self.columns_ext.get(col)
            col_ext_name = col_ext if col_ext else col
            ws.write(0,index,col_ext_name.decode('utf8'))
        #写入内容
        for index,data in enumerate(self.data_list):
            for col_index,col in enumerate(self.columns):
                ws.write(index+1,col_index,str(data.get(col,self.fill_none)).decode('utf8'))
        bio = BytesIO()
        wb.save(bio)
        return bio


#BytesIo操作的时二进制数据，用于将数据写入到本地硬盘, string操作的是字符串，不写入本地硬盘

#在具体使用过程中 要用self.write(bio.getvalue())





