# import logging
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



url3 = 'http://service.picasso.adesk.com/v1/wallpaper/album/'
url1 = 'http://service.picasso.adesk.com/v1/wallpaper/category/'

usar_agent = 'Dalvik/2.1.0 (Linux; U; Android 7.0; ZUK Z2121 Build/NRD90M)'
headers = {'User-Agent': usar_agent}
usar_agent_json = 'picasso,186,tencent'
headers_json = {'User-Agent': usar_agent_json}
#eg :http://service.picasso.adesk.com/v1/wallpaper/category/4e4d610cdf714d2966000000/wallpaper?limit=20&skip=0&adult=true&first=1&order=hot
# url_data

socket.setdefaulttimeout(random.uniform(1, 5))
def isWindowsSystem():
    return 'Windows' in platform.system()
def isLinuxSystem():
    return 'Linux' in platform.system()

##################################变量区##############################
# linux地址
linux_foldername1 = '//mnt//samba//ALL/newdownload//安卓壁纸//专辑//'
# windows地址
windows_foldername1 = 'E:\\网站\\安卓壁纸\\专辑\\'

if isWindowsSystem() == True:
    foldername = windows_foldername1
if isLinuxSystem() == True:
    foldername = linux_foldername1
pool_size = multiprocessing.cpu_count() #进程数量
# pool_size =1
delay_timne =1             #下载延迟时间
# =======json—data数据========
json_url = url1
json_type = '4e4d610cdf714d2966000000'
paper_type = 'album'      #wallpaper or vertical
limit = '40'
adult = 'false'
first = '1'
order = 'new'               #hot or new
# =======json—data数据========

bigan_number = 0       #开始寻找专题的参数
end_number = 10000    #结束寻找专题的参数
bigan_imgnumber= 0         #开始寻找专题内文件的参数
end_imgnumber = 10000    #结束寻找专题内文件的参数


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
bigan_id ='"id":'         #开始搜索关键字
end_id = '"'               #结束搜索关键字
bigan_id_num=7             #删除开头字符数
end_id_num=0                #删除结尾字符数
##################################变量区##############################



def get_json(get_url,isheaders_json):
    try:
        url = get_url
        data = None
        if isheaders_json=='true':
            get_json_headers = headers_json
        else:
            get_json_headers = headers
        print(get_json_headers)
        # logger.info(get_json_headers)
        req = urllib.request.Request(url, data, get_json_headers)
        response = urllib.request.urlopen(req, timeout=2)

    except http.client.error as e:
        print(get_url + '访问页面出错clienterror ')
        # logger.info(get_url + '访问页面出错clienterror ')
        return 'false'
    except urllib.error.HTTPError as e:
        print(get_url + '访问页面出错HTTPError')
        # logger.info(get_url + '访问页面出错HTTPError')
        return 'false'
    except urllib.error.URLError as e:
        print(get_url + '访问页面出错URLError')
        # logger.info(get_url + '访问页面出错URLError')
        return 'false'
    else:
        return response.read()


def find_json(json_url,isheader):
    ALLimgfolder_info = [[]]  #建立空的数组
    # json_data=get_json(json_url).decode('utf-8')
    temp = get_json(json_url, isheader)
    if temp =='false':
        return ALLimgfolder_info
    # json_data = temp.decode('unicode_escape')
    json_data = temp.decode('unicode_escape')
    # print(json_data)

    if isheader =='false':
        a_user = json_data.find('"user":')
        b_user = json_data.find('},', a_user)
        # print(json_data)
        a_id = json_data.find('"id":')
        a_name = json_data.find('"name":')
        if not (a_id < a_user or a_id > b_user):
            a_id = json_data.find('"id":', b_user)
        if  not (a_name < a_user or a_name > b_user):
            a_name = json_data.find('"name":', b_user)

        while a_id != -1:
            img_info = []
            b_id = a_id+31
            b_name = json_data.find('"',a_name+9)
            # 保存专辑信息
            img_id=json_data[a_id + 7:b_id]
            img_name = json_data[a_name+9:b_name]
            img_name = re.sub("[\s+\.\!\/_$%^*(+\"\')]+|[+——！【】「」。？、~@#￥%……&*（）]", "", img_name)
            print(img_id+'_'+img_name)
            # logger.info(img_id+'_'+img_name)
            img_info.append(img_id)
            img_info.append(img_name)
            ALLimgfolder_info.append(img_info)
            # 继续找
            a_name = json_data.find('"name":', b_name)
            if a_id>b_user :
                a_id = json_data.find('"id":', b_id)
            else:
                a_id = json_data.find('"id":', b_user)
            if a_name > b_user:
                a_name = json_data.find('"name":', b_name)
            else:
                a_name = json_data.find('"name":', b_user)
            a_user = json_data.find('"user":', b_user)
            b_user = json_data.find('},', a_user)
            # a_desc = json_data.find('"desc":',a_desc)
            # 判断是否不在usar里
            if not (a_id < a_user or a_id > b_user):
                if a_id !=-1:
                    a_id = json_data.find('"id":', b_user)
            if not (a_name < a_user or a_name > b_user):
                a_name = json_data.find('"name":', b_user)
    else:
        wallpaper = json_data.find('"wallpaper"')
        a_img_user = json_data.find('"user"',wallpaper)
        # print(a_img_user)
        b_img_user = json_data.find('},', a_img_user)
        # print(b_img_user)
        a_img_img = json_data.find(bigan_img)
        a_img_tag = json_data.find(bigan_tag,wallpaper)
        a_img_id = json_data.find(bigan_id,wallpaper)
        if not (a_img_id < a_img_user or a_img_id > b_img_user):
            a_img_id = json_data.find('"id":', b_img_user)
        # 不带停，如果没找到则退出循环
        while a_img_id != -1:
            img_info = []
            # 以a的位置为起点的图片
            b_img_img = json_data.find(end_img, a_img_img)
            b_img_tag = json_data.find(end_tag, a_img_tag)
            b_img_id = a_img_id+31
            # json关键字名称输出
            img_down = json_data[a_img_img + bigan_img_num:b_img_img + end_img_num]
            img_tag = json_data[a_img_tag + bigan_tag_num:b_img_tag + end_tag_num]
            img_tag = re.sub("[\s+\.\!\/_$%^*(+\"\')]+|[+——！【】「」。？、~@#￥%……&*（）]", "", img_tag)
            img_id = json_data[a_img_id + bigan_id_num:b_img_id + end_id_num]
            # 如果找到就添加到图片列表中
            if b_img_img != -1:
                img_info.append(img_id)
                img_info.append(img_tag)
                img_info.append(img_down)
                ALLimgfolder_info.append(img_info)
            # 否则偏移下标
            else:
                b_img_img = a_img_img + 9
            print(img_id + "_img_" + img_tag)  # 图片id图片标签
            print(img_down)#图片下载地址
            # logger.info(img_id + "_img_" + img_tag)
            # logger.info(img_down)
            # 继续找
            a_img_img = json_data.find(bigan_img, b_img_img)
            a_img_tag = json_data.find(bigan_tag, b_img_tag)
            a_img_id = json_data.find(bigan_id, b_img_id)
            if a_img_id != -1:
                if a_img_id>b_img_user :
                    a_img_id = json_data.find('"id":', b_img_id)
                else:
                    a_img_id = json_data.find('"id":', b_img_user)
            a_img_user = json_data.find('"user":', b_img_user)
            b_img_user = json_data.find('},', a_img_user)
            # 判断是否不在usar里
            if not (a_img_id < a_img_user or a_img_id > b_img_user):
                if a_img_id != -1:
                    a_img_id = json_data.find('"id":', b_img_user)
    return ALLimgfolder_info

def download_img(folderlist,ALLimg_temp):
    # 输出文件
    for j in range(1,len(ALLimg_temp)):
        n=0
        if ALLimg_temp[j][1]=='' :
            ALLimg_temp[j][1]='无'
        filelist = folderlist + ALLimg_temp[j][0] +'_'+ ALLimg_temp[j][1]+".jpg"
        # 下载文件
        if not os.path.exists(filelist):
            sleep(delay_timne)
            try:
                data = None
                req = urllib.request.Request(ALLimg_temp[j][2], data, headers)
                response = urllib.request.urlopen(req, timeout=2)
                # print(req)
                # print(response)
                print(ALLimg_temp[j][2] + ' '+ ALLimg_temp[j][1]+'         OK')
                # logger.info(ALLimg_temp[j][2] + ' '+ ALLimg_temp[j][1]+'         OK')
                try:
                    file_data = response.read()
                    with open(filelist, 'wb') as response:
                        response.write(file_data)
                        response.close()
                        continue
                except IOError:
                    print(filelist + "写入错误 \n")
                    # logger.info(filelist + "写入错误 \n")
                    continue
            except http.client.error as e:
                print(ALLimg_temp[j][2] + '访问页面出错clienterror')
                # logger.info(ALLimg_temp[j][2] + '访问页面出错clienterror')
                continue
            except urllib.error.HTTPError as e:
                print(ALLimg_temp[j][2] + '访问页面出错HTTPError')
                # logger.info(ALLimg_temp[j][2] + '访问页面出错HTTPError')
                continue
            except urllib.error.URLError as e:
                print(ALLimg_temp[j][2] + '访问页面出错URLError')
                # logger.info(ALLimg_temp[j][2] + '访问页面出错URLError')
                continue
            #     n += 1
            # if n > 3:                      v
            #     # print(filelist + "已存在")
            #     break
        else:
            print(filelist + "已存在")
            # logger.info(filelist + "已存在")

def check_foldertype(i):
    print("==================任务开始===================")

    str_i = str(i)
    url = json_url + json_type +'/'+paper_type+'?limit='+limit+ '&skip=' + str_i + '&adult='+adult+'&first='+first+'&order='+order
    print(url)
    # logger.info(url)
    ALLfolder_temp = find_json(url,'false')

    for j in range(1,len(ALLfolder_temp)):
        if len(ALLfolder_temp) == 1:
            return
        if ALLfolder_temp[j][1] == '':
            ALLfolder_temp[j][1] ='临时'
        if isWindowsSystem()==True :
            folderlist = foldername + ALLfolder_temp[j][1] + '\\'
        if isLinuxSystem() == True:
            folderlist = foldername + ALLfolder_temp[j][1] + '//'
        check_imgtype(ALLfolder_temp[j][0], folderlist)



def check_imgtype(downlist,folderlist):
    # 检测文件夹
    print(folderlist)
    if os.path.exists(folderlist):
        print(folderlist + '文件夹已存在')
        # logger.info(folderlist + '文件夹已存在')
    else:
        # 创建目录操作函数


        os.mkdir(folderlist)
        print(folderlist + '文件夹创建成功')
        # logger.info(folderlist + '文件夹创建成功')
    for i in range(bigan_imgnumber,end_imgnumber):
        if not i % 40:
            str_i = str(i)
            imt_url = url3 +downlist+'/'+'wallpaper'+'?limit='+limit+ '&skip=' + str_i + '&adult='+adult+'&first='+first+'&order='+order
            print(imt_url)
            # logger.info(imt_url)
            ALLimg_temp = find_json(imt_url,'true')
            if len(ALLimg_temp) == 1:
                return
            download_img(folderlist,ALLimg_temp)



def start_run():
    testFL = []
    for i in range(bigan_number,end_number):
        if not i % 40:
            testFL.append(i)
            # check_foldertype(i)
    pool = multiprocessing.Pool(processes=pool_size)
    print(pool_size)
    for i in testFL:
        msg = i
        print(i)
        pool.apply_async(check_foldertype, (msg,))
    pool.close()
    pool.join()
if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    start_run()
    print("====================代码执行完毕==========================")
    # logger.info("====================代码执行完毕==========================")
