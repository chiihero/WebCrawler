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

# # 查询数据
# sql = "SELECT name " \
#       "FROM picture_info " \
#       "WHERE dowmload = '%d' "
# data = (0)
# cursor.execute(sql % data)
# for row in cursor.fetchall():
#     print("Name:%s\t" % row)
# print('共查找出', cursor.rowcount, '条数据')

sql = "INSERT INTO picture_info (name, link, tag, type, source) VALUES ( '%s', '%s', '%s' , '%s', '%s' )"
data = ('雷军' + str(i), 'baidu.com', '傻娃子' + str(i))
cursor.execute(sql % data)
connect.commit()
print('成功插入', cursor.rowcount, '条数据')

cursor.close()
connect.close()
