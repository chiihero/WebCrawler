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


# 本地地址
windows_foldername1 = 'E:\\哔哩哔哩\\'
# wifi网络地址，需要先加入磁盘映射
linux_foldername1 = '//mnt//samba//安卓壁纸//'
if isWindowsSystem() == True:
    foldername = windows_foldername1
if isLinuxSystem() == True:
    foldername = linux_foldername1

##################################变量区##############################
# pool_size = multiprocessing.cpu_count() #进程数量
pool_size =1
# =======json—data数据========
json_url = url1
category = cos
type = 'hot'               #hot or new
page_size = '10'
# adult = 'false'
# first = '1'

# =======json—data数据========

bigan_number = 0         #开始寻找json的参数
end_number = 25           #结束寻找json的参数
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
        print(e.reason)

    except urllib.error.HTTPError as e:
        print(e.reason)

    except urllib.error.URLError as e:
        print(e.reason)
    else:
        return response.read()


def find_json(find_i,json_url):
    ALLimg_info = [[]]  #建立空的数组
    # json_data=get_json(json_url).decode('utf-8')
    # json_data = get_json(json_url).decode('unicode_escape')
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
        img_name = re.sub("[\s+\.\!\/_$%^*|?:(+\"\')<>/]+|[+——！，。？、~@#￥%……&*（）]", "", img_name)
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

def download_img(temp,folderlist):
    for i in range(1, 21):
        # 检测文件夹
        # print(folderlist)
        folderlist_temp = folderlist +temp[i][0] + '\\'
        if os.path.exists(folderlist_temp):
            print(folderlist_temp + '文件夹已存在')
        else:
            # 创建目录操作函数
            os.mkdir(folderlist_temp)
            print(folderlist_temp + '文件夹创建成功')

        # 输出文件
        for j in range(2,len(temp[i])) :
            n=0
            str_j = str(j - 1)
            filelist = folderlist_temp + temp[i][1] +'_'+ str_j+".jpg"

            # print(temp[i][j])
            # print(filelist)

            # 下载文件
            if not os.path.exists(filelist):
                sleep(delay_timne)
                try:
                    data = None
                    req = urllib.request.Request(temp[i][j], data, headers)
                    response = urllib.request.urlopen(req, timeout=2)
                    # print(req)
                    # print(response)
                    print(temp[i][j] + ' '+ temp[i][1]+'         OK')
                    try:
                        file_data = response.read()
                        with open(filelist, 'wb') as response:
                            response.write(file_data)
                            response.close()
                            continue
                    except IOError:
                        print(temp[i][j] + ' '+ temp[i][1] + "\n"+filelist+"写入错误 \n")
                        continue
                except http.client.error as e:
                    print(e.reason)
                    continue
                except urllib.error.HTTPError as e:
                    print(e.reason)
                    continue
                except urllib.error.URLError as e:
                    print(e.reason)
                    continue
            else:
                pass
                # print(filelist + "已存在")

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
            if isWindowsSystem() == True:
                folderlist = foldername + def_type_name[i] + "\\" + type + "\\"
            if isLinuxSystem() == True:
                folderlist = foldername + def_type_name[i] + "//" + type + "//"
            print(folderlist)
            download_img(ALLfolder_temp, folderlist)

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
