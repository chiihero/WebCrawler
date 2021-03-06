# -*- coding: utf-8 -*-

# 数据库设计方案
# CREATE TABLE `picture_info` (
#   `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
#   `name` varchar(40) NOT NULL COMMENT '图片名称',
#   `title` varchar(20) NOT NULL COMMENT '图片标题',
#   `link` varchar(120) NOT NULL COMMENT '图片链接',
#   `tag` varchar(50) NOT NULL COMMENT '图片标签',
#   `type` varchar(10) NOT NULL COMMENT '类型',
#   `author` varchar(20) NOT NULL COMMENT '作者',
#   `source` varchar(20) NOT NULL COMMENT '来源',
#   `datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
#   `dowmload` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否已经下载',
#   `wrong` int(4) unsigned NOT NULL DEFAULT '0' COMMENT '下载错误次数',
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=3519 DEFAULT CHARSET=utf8


import os
import sys
import urllib.request
import urllib
import urllib.error
import http.client
import multiprocessing
import random
import socket
import pymysql
import re
from time import time, sleep
import platform

def isWindowsSystem():
    return 'Windows' in platform.system()
def isLinuxSystem():
    return 'Linux' in platform.system()

def_type = ['sifu', 'cos']
def_type_name = ['私服','cos']
# 美女链接
girl = def_type[0]
# cos链接
cos = def_type[1]


usar_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'
headers = {'User-Agent': usar_agent}
#eg :http://api.vc.bilibili.com/link_draw/v2/Photo/list?category=cos&type=hot&page_size=0&page_size=20
# url_data
socket.setdefaulttimeout(random.uniform(1, 5))

# 壁纸
url1 = 'http://api.vc.bilibili.com/link_draw/v2/Photo/list?category='


##################################变量区##############################
# pool_size = multiprocessing.cpu_count() #进程数量
pool_size =1
# =======json—data数据========
json_url = url1
category = girl
p_type = 'cos'
type = 'hot'               #hot or new
page_size = '10'
# adult = 'false'
# first = '1'

# =======json—data数据========



bigan_number = 0         #开始寻找json的参数
end_number = 30           #结束寻找json的参数
delay_timne =0             #下载延迟时间

# 下载文件名搜索
bigan_name = '"name":'  # 开始搜索关键字
end_name = '"},'  # 结束搜索关键字
bigan_name_num = 8  # 删除开头字符数
end_name_num = 0  # 删除结尾字符数
# 下载地址搜索
bigan_img = '"img_src"'  # 开始搜索关键字
end_img = '",'  # 结束搜索关键字
bigan_img_num = 11  # 删除开头字符数
end_img_num = 0  # 删除结尾字符数
# 下载title搜索
bigan_title = '"title":'  # 开始搜索关键字
end_title = '",'  # 结束搜索关键字
bigan_title_num = 8  # 删除开头字符数
end_title_num = 0  # 删除结尾字符数
##################################变量区##############################


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


def get_json(get_url):
    try:
        url = get_url
        data = None
        req = urllib.request.Request(url, data, headers)
        response = urllib.request.urlopen(req, timeout=2)
    except http.client.error as e:
        print(e.reason)
    except urllib.error.HTTPError as e:
        print(e.reason)

    except urllib.error.URLError as e:
        print(e.reason)
    else:
        return response.read()


def find_json(find_i,json_url):
    ALLimg_info = [[]]  #建立空的数组

    json_data = get_json(json_url).decode('utf-8')
    # print(json_data)
    a_name = json_data.find(bigan_name)
    a_img = json_data.find(bigan_img)
    a_title =  json_data.find(bigan_title)
    # 不带停，如果没找到则退出循环
    while a_img != -1:
        img_info = []
        # 以a的位置为起点的图片
        b_name = json_data.find(end_name,a_name)
        img_name = json_data[a_name + bigan_name_num:b_name + end_name_num]
        img_name=re.sub("[\s+\.\!\/_$%^*|?:(+\"\')<>/]+|[+——！，。？、~@#￥%……&*（）]","",img_name)
        img_info.append(img_name)
        # print(img_name)  # 图片标签
        b_title = json_data.find(end_title, a_title)
        # json关键字名称输出
        img_title = json_data[a_title + bigan_title_num:b_title + end_title_num]
        img_title=re.sub("[\s+\.\!\/_$%^*|?:(+\"\')<>/]+|[+——！，。？、~@#￥%……&*（）]","",img_title)
        img_info.append(img_title)
        # print(img_title)  # 图片id图片标签

        while a_img<a_title and a_img!=-1:
            b_img = json_data.find(end_img, a_img)
            if b_img!=-1:
                img_down = json_data[a_img + bigan_img_num:b_img + end_img_num]
                img_info.append(img_down)
                # print(img_down)  # 图片下载地址
            a_img = json_data.find(bigan_img, b_img)

        # 如果找到就添加到图片列表中
        ALLimg_info.append(img_info)

        # print(img_title+"_"+img_name)  # 图片id图片标签
        # print(img_down)#图片下载地址
        # 继续找
        a_img=json_data.find(bigan_img,b_img)
        a_name = json_data.find(bigan_name,b_name)
        a_title = json_data.find(bigan_title,b_title)

    return ALLimg_info
# img_info[i][0]图片作者img_info[i][1]图片标题img_info[i][j]链接
def insert_img(img_info):
    for i in range(1, 21):
        for j in range(2,len(img_info[i])) :
            p_name = img_info[i][j].split('/')[-1].split('.')[0]
            print(p_name)
            # 查询数据
            sql = "SELECT name FROM picture_info WHERE link = '%s' "
            data = (img_info[i][j])
            cursor.execute(sql % data)
            if (cursor.fetchall()):
                print('重复数据')
                continue
            else:
                sql = "INSERT INTO picture_info (name, title, link, tag, type, author, source) VALUES ('%s', '%s', '%s', '%s', '%s' , '%s', '%s' )"
                data = (p_name,img_info[i][1],img_info[i][j], p_type ,'美女',img_info[i][0],'哔哩哔哩' )
                cursor.execute(sql % data)
                connect.commit()
                print('成功插入'+img_info[i][j])


def check_type(i):
    str_i = str(i)
    url = json_url + category + '&type='+type+ '&page_num='+str_i +'&page_size=' +page_size
    print(url)

    ALLfolder_temp = find_json(i, url)
    print("==============================================")
    # 判断类型
    for i in range(2):
        # print(category)
        # print(def_type[i])
        if len(ALLfolder_temp) == 1:
            return
        if category in def_type[i]:  # 美女
            insert_img(ALLfolder_temp)

def start_run():
    testFL = []

    for i in range(bigan_number,end_number):
            testFL.append(i)
    pool = multiprocessing.Pool(processes=pool_size)
    print(pool_size)
    for i in testFL:
        msg = i
        pool.apply_async(check_type, args=(msg,))
    pool.close()
    pool.join()

if __name__ == '__main__':

    start_run()

    print("====================代码执行完毕==========================")
    cursor.close()
    connect.close()
