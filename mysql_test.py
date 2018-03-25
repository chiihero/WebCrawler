# -*- coding: utf-8 -*-
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

type = ['4e4d610cdf714d2966000000', '4e4d610cdf714d2966000003', '4e4d610cdf714d2966000002', '4e4d610cdf714d2966000007', '5109e04e48d5b9364ae9ac45', '4fb479f75ba1c65561000027', '4ef0a35c0569795756000000', '4fb47a195ba1c60ca5000222', '5109e05248d5b9368bb559dc', '4fb47a465ba1c65561000028', '4ef0a3330569795757000000', '4e4d610cdf714d2966000006', '4e4d610cdf714d2966000005', '4e4d610cdf714d2966000004', '4fb47a305ba1c60ca5000223', '4e4d610cdf714d2966000001', '4ef0a34e0569795757000001', '4e58c2570569791a19000000']
type_name = ['美女','动漫','风景','游戏','文字','视觉','情感','设计','明星','物语','艺术','男人','机械','卡通','城市','动物','运动','影视']
# 美女链接
girl = type[0]
# 动漫链接
animation = type[1]
# 风景链接
landscape = type[2]
# 游戏链接
game = type[3]
# 文字链接
text = type[4]
# 视觉链接
vision = type[5]
# 情感链接
emotion = type[6]
# 设计链接
creative = type[7]
# 明星链接
celebrity = type[8]
# 物语链接
stuff = type[9]
# 艺术链接
art = type[10]
# 男人链接
man = type[11]
# 机械链接
machine = type[12]
# 卡通链接
cartoon = type[13]
# 城市链接
cityscape = type[14]
# 动物链接
animal = type[15]
# 运动链接
sport = type[16]
# 影视链接
movie = type[17]

usar_agent = 'Dalvik/2.1.0 (Linux; U; Android 7.0; ZUK Z2121 Build/NRD90M)'
headers = {'User-Agent': usar_agent}
usar_agent_json = 'picasso,186,tencent'
headers_json = {'User-Agent': usar_agent_json}
#eg :http://service.picasso.adesk.com/v1/wallpaper/category/4e4d610cdf714d2966000000/wallpaper?limit=20&skip=0&adult=true&first=1&order=hot
# url_data
socket.setdefaulttimeout(random.uniform(1, 5))

# 横向壁纸
url1 = 'http://service.picasso.adesk.com/v1/wallpaper/category/'
# 竖屏壁纸
url2 = 'http://service.picasso.adesk.com/v1/vertical/category/'

##################################变量区##############################
# pool_size = multiprocessing.cpu_count() #进程数量
pool_size =1
# =======json—data数据========
p_type = 'wallpaper'
p_source='安卓壁纸'
json_url = url1
json_type = girl
paper_type = 'wallpaper'      #wallpaper or vertical
limit = '20'
adult = 'false'
first = '1'
order = 'hot'               #hot or new
# =======json—data数据========



bigan_number = 0         #开始寻找json的参数
end_number = 20000           #结束寻找json的参数
delay_timne =0             #下载延迟时间

# 下载地址搜索
bigan_img = '"wp":'         #开始搜索关键字
end_img =  '",'             #结束搜索关键字
bigan_img_num=7             #删除开头字符数
end_img_num=0               #删除结尾字符数
# 下载标签搜索
bigan_tag ='"tag":'         #开始搜索关键字
end_tag ='],'               #结束搜索关键字
bigan_tag_num=8             #删除开头字符数
end_tag_num=0               #删除结尾字符数
# 下载desc搜索
bigan_desc ='"desc":'         #开始搜索关键字
end_desc = '"}'               #结束搜索关键字
bigan_desc_num=9              #删除开头字符数
end_desc_num=0                #删除结尾字符数
# 下载id搜索
bigan_id ='"id": "'         #开始搜索关键字
end_id = '",'               #结束搜索关键字
bigan_id_num=7              #删除开头字符数
end_id_num=0                #删除结尾字符数
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
    json_data = get_json(json_url).decode('unicode_escape')

    a_img = json_data.find(bigan_img)
    a_tag = json_data.find(bigan_tag)
    a_desc = json_data.find(bigan_desc)
    a_id = json_data.find(bigan_id)
    # 不带停，如果没找到则退出循环
    while a_img != -1:
        img_info = []
        # 以a的位置为起点的图片
        b_img = json_data.find(end_img,a_img)
        b_tag = json_data.find(end_tag,a_tag)
        b_desc = json_data.find(end_desc, a_desc)
        b_id = json_data.find(end_id, a_id)
        # json关键字名称输出
        img_down = json_data[a_img + bigan_img_num:b_img + end_img_num]
        img_tag = json_data[a_tag+bigan_tag_num:b_tag+end_tag_num]
        img_tag=re.sub("[\s+\.\!\/_$%^*(+\"\')]+|[+——！，。？、~@#￥%……&*（）]","",img_tag)
        img_id = json_data[a_id + bigan_id_num:b_id + end_id_num]
        img_desc = json_data[a_desc + bigan_desc_num:b_desc + end_desc_num]
        # 如果找到就添加到图片列表中
        if b_img != -1:
            img_info.append(img_id)
            img_info.append(img_down)
            img_info.append(img_tag)
            img_info.append(img_desc)
            ALLimg_info.append(img_info)
        # 否则偏移下标
        else:
            b_img=a_img+9
        # print("文件信息"+img_id+"\n"+img_down+"\n"+img_tag+"\n"+img_desc)  # 图片id图片标签
        # print(img_down)#图片下载地址
        # 继续找
        a_img=json_data.find(bigan_img,b_img)
        a_tag = json_data.find(bigan_tag,b_tag)
        a_desc = json_data.find(bigan_desc,b_desc)
        a_id = json_data.find(bigan_id, b_id)

    return ALLimg_info
# img_info[i][0]图片名字img_info[i][1]图片链接img_info[i][2]图片标签
def insert_img(img_info):
    for i in range(1, 21):
        for j in range(2,len(img_info[i])) :
            # 查询数据
            sql = "SELECT name FROM picture_info WHERE link = '%s' "
            data = (img_info[i][j])
            cursor.execute(sql % data)
            if (cursor.fetchall()):
                print('重复数据')
                continue
            else:
                sql = "INSERT INTO picture_info (name, link, tag, type, author, source) VALUES ('%s', '%s', '%s', '%s' , '%s', '%s' )"
                data = (img_info[i][0],img_info[i][1],img_info[i][2], p_type ,img_info[i][3],p_source )
                cursor.execute(sql % data)
                connect.commit()
                print('成功插入'+img_info[i][0]+img_info[i][2])

def check_type(i):
    str_i = str(i)
    url = json_url + json_type +'/'+paper_type+'?limit='+limit+ '&skip=' + str_i + '&adult='+adult+'&first='+first+'&order='+order
    print(url)
    temp = find_json(i, url)
    print("==============================================")
    # 判断类型
    for i in range(17):
        if json_type in type[i]:  # 美女
            insert_img(temp)

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
