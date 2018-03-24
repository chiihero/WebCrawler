# -*- coding: utf-8 -*-
import os
import urllib.request
import urllib
import urllib.error
import http.client
import multiprocessing
import random
import socket
import csv
import signal
import json
import unicodedata
import re
from time import time, sleep
import platform

def isWindowsSystem():
    return 'Windows' in platform.system()
def isLinuxSystem():
    return 'Linux' in platform.system()

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
# 本地地址
windows_foldername1 = 'e:\\网站\\安卓壁纸\\'

# wifi网络地址，需要先加入磁盘映射
linux_foldername1 = '//mnt//samba//安卓壁纸//'
if isWindowsSystem() == True:
    foldername = windows_foldername1
if isLinuxSystem() == True:
    foldername = linux_foldername1

##################################变量区##############################
# pool_size = multiprocessing.cpu_count() #进程数量
pool_size = 3
# =======json—data数据========
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
# 下载id搜索
bigan_id ='"id": "'         #开始搜索关键字
end_id = '",'               #结束搜索关键字
bigan_id_num=7              #删除开头字符数
end_id_num=0                #删除结尾字符数
##################################变量区##############################




def get_json(get_url):
    try:
        url = get_url
        data = None
        req = urllib.request.Request(url, data, headers)
        response = urllib.request.urlopen(req, timeout=2)
        # 将json转换成字典
        # json_data = response.read()
        # temp=json.loads(json_data)
        # print(temp['res']['wallpaper'])
        # return temp['res']['wallpaper']

    except http.client.error as e:
        print(ALLimg_temp[j][2] + '访问页面出错clienterror ')

    except urllib.error.HTTPError as e:
        print(ALLimg_temp[j][2] + '访问页面出错HTTPError')

    except urllib.error.URLError as e:
        print(ALLimg_temp[j][2] + '访问页面出错URLError')
    else:
        return response.read()


def find_json(find_i,json_url):
    ALLimg_info = [[]]  #建立空的数组
    # json_data=get_json(json_url).decode('utf-8')
    json_data = get_json(json_url).decode('unicode_escape')
    a_img = json_data.find(bigan_img)
    a_tag = json_data.find(bigan_tag)
    a_id =  json_data.find(bigan_id)
    # 不带停，如果没找到则退出循环
    while a_img != -1:
        img_info = []
        # 以a的位置为起点的图片
        b_img = json_data.find(end_img,a_img)
        b_tag = json_data.find(end_tag,a_tag)
        b_id = json_data.find(end_id, a_id)
        # json关键字名称输出
        img_down = json_data[a_img + bigan_img_num:b_img + end_img_num]
        img_tag = json_data[a_tag+bigan_tag_num:b_tag+end_tag_num]
        img_tag=re.sub("[\s+\.\!\/_$%^*(+\"\')]+|[+——！，。？、~@#￥%……&*（）]","",img_tag)
        img_id = json_data[a_id + bigan_id_num:b_id + end_id_num]
        # 如果找到就添加到图片列表中
        if b_img != -1:
            img_info.append(img_id)
            img_info.append(img_tag)
            img_info.append(img_down)
            ALLimg_info.append(img_info)
        # 否则偏移下标
        else:
            b_img=a_img+9
        print(img_id+"_"+img_tag)  # 图片id图片标签
        # print(img_down)#图片下载地址
        # 继续找
        a_img=json_data.find(bigan_img,b_img)
        a_tag = json_data.find(bigan_tag,b_tag)
        a_id = json_data.find(bigan_id,b_id)

    return ALLimg_info

def download_img(temp,folderlist):
    # 检测文件夹
    print(folderlist)
    if os.path.exists(folderlist):
        print(folderlist + '文件夹已存在')
    else:
        # 创建目录操作函数
        os.mkdir(folderlist)
        print(folderlist + '文件夹创建成功')
    # 输出文件
    for j in range(1,20):
        n=0
        if temp[j][1]=='' :
            temp[j][1]='无'
        filelist = folderlist + temp[j][0] +'_'+ temp[j][1]+".jpg"
        # 下载文件
        if not os.path.exists(filelist):
            sleep(delay_timne)

            try:
                data = None
                req = urllib.request.Request(temp[j][2], data, headers)
                response = urllib.request.urlopen(req, timeout=2)
                # print(req)
                # print(response)
                print(temp[j][2] + ' '+ temp[j][1]+'         OK')
                try:
                    file_data = response.read()
                    with open(filelist, 'wb') as response:
                        response.write(file_data)
                        response.close()
                        continue
                except IOError:
                    print(filelist + "写入错误 \n")
                    continue
            except http.client.error as e:
                print(ALLimg_temp[j][2] + '访问页面出错clienterror ')
                continue
            except urllib.error.HTTPError as e:
                print(ALLimg_temp[j][2] + '访问页面出错HTTPError')
                continue
            except urllib.error.URLError as e:
                print(ALLimg_temp[j][2] + '访问页面出错URLError')
                continue
        else:
            print(filelist + "已存在")

def check_type(i):

    str_i = str(i)
    url = json_url + json_type +'/'+paper_type+'?limit='+limit+ '&skip=' + str_i + '&adult='+adult+'&first='+first+'&order='+order
    print(url)
    temp = find_json(i, url)
    print("==============================================")
    # 判断类型
    for i in range(17):
        if json_type in type[i]:  # 美女
            if isWindowsSystem() == True:
                folderlist = foldername + type_name[i] + "\\" + paper_type + "\\" + order + "\\"
            if isLinuxSystem() == True:
                folderlist = foldername + type_name[i] + "//" + paper_type + "//" + order + "//"
            print(folderlist)
            download_img(temp, folderlist)

def start_run():
    testFL = []
    for i in range(bigan_number,end_number):
        if not i % 20:
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
