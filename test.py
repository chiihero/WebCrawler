#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os,sys
import pymysql
# 打开数据库连接
try:
    connect = pymysql.connect(
        host='139.199.11.57',
        port=3306,
        user='webcrawler',
        password='webcrawler1',
        database='webcrawler',
        charset='utf8'
    )
except Exception as e:
    print (e)
    sys.exit()
# 获取游标
cursor = connect.cursor()
# 插入数据
# # 查询数据
# sql = "SELECT name FROM picture_info WHERE account = '%s' "
# data = ('13512345678',)
# cursor.execute(sql % data)
# for row in cursor.fetchall():
#     print("Name:%s\tSaving:%.2f" % row)
# print('共查找出', cursor.rowcount, '条数据')
# #
# # 修改数据
# sql = "UPDATE picture_info SET dowmload = %d WHERE name = '%s' "
# data = (1, '雷军2')
# cursor.execute(sql % data)
# connect.commit()
# print('成功修改', cursor.rowcount, '条数据')

cursor.close()
connect.close()
