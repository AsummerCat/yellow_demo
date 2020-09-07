# -*- coding: utf-8 -*-

'''
管道下载
'''
import json
import multiprocessing
import os
import platform
import re
import uuid
import datetime
import time

import requests
from pyaria2 import Aria2RPC
from yellow_download.settings import MAC_DOWNLOAD_PATH
from yellow_download.settings import WIN_DOWNLOAD_PATH
import m3_dl
from multiprocessing import Pool

'''
YellowDownload的管道 start   =>aria2调用
'''


class YellowDownloadPipeline(object):
    def process_item(self, item, spider):
        title = "".join(re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+', item['title'], re.S))
        path = ""
        info_os = check_os()
        if "Windows" == info_os:
            path = WIN_DOWNLOAD_PATH
        elif "macOS" == info_os:
            path = MAC_DOWNLOAD_PATH
        else:
            print("暂未识别系统无法下载内容")
        # 下载本地目录
        item["file_path"] = path
        # 判断文件夹是否存在 不存在直接makedirs 创建多级目录
        if not os.path.exists(path):
            os.makedirs(path)
        # 获取下载的文件名称
        if not len(title) > 0:
            title = str(uuid.uuid1()) + ".mp4"
        else:
            title = title + ".mp4"
        item["title"] = title
        info_down_path = path + "/" + title

        item["info_down_path"] = info_down_path
        if not os.path.exists(info_down_path):
            print("开始下载:{}".format(title))
            self.addTask(item=item)
            time.sleep(20)
        else:
            print(title + "====================>>>>已存在")
        return item

    '''
    添加下载任务
    '''

    def addTask(self, item):

        title = item["title"]
        down_path = item["down_path"]
        info_down_path = item["info_down_path"]
        path = item["file_path"]
        print("名称:{}=================下载地址:{}".format(title, info_down_path))
        self.get_file_from_url(path, down_path, title)

    # 根据文件链接+文件名称 添加下载任务
    def get_file_from_url(self, path, link, file_name):
        info_os = check_os()
        if "Windows" == info_os:
            get_file_from_url_by_windows(path, link, file_name)
        elif "macOS" == info_os:
            get_file_from_url_by_mac(path, link, file_name)
        else:
            print("暂未识别系统无法下载内容")


def get_file_from_url_by_windows(path, link, file_name):
    jsonrpc = Aria2RPC()
    options = {"dir": path, "out": file_name, }
    res = jsonrpc.addUri([link], options=options)


# json形式根据文件链接+文件名称 添加下载任务
def get_file_from_url_by_mac(path, link, file_name):
    options = {"dir": path, "out": file_name}
    params = [[link], options]
    url = "http://localhost:6800/jsonrpc"
    jsonreq = json.dumps({'jsonrpc': '2.0', 'id': 'qwer',
                          'method': 'aria2.addUri',
                          "params": params})
    requests.post(url, jsonreq)


'''
YellowDownload的管道 end 
'''


# 检查当前系统
def check_os():
    sysstr = platform.system()

    if (sysstr == "Windows"):
        return "Windows"
    elif (sysstr == "Linux"):
        return "linux"
    elif (sysstr == "Darwin"):
        return "macOS"
    else:
        return "other"


'''
Mienav的管道 使用 ffmpeg
'''


# 开启多线程下载
def go_thread_download(item):
        title = "".join(re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+', item['title'][0], re.S))
        starttime_wm = time.time()
        path = ""
        info_os = check_os()
        if "Windows" == info_os:
            path = WIN_DOWNLOAD_PATH
        elif "macOS" == info_os:
            path = MAC_DOWNLOAD_PATH
        else:
            print("暂未识别系统无法下载内容")
            return
        # 下载本地目录
        item["file_path"] = path
        # 判断文件夹是否存在 不存在直接makedirs 创建多级目录
        if not os.path.exists(path):
            os.makedirs(path)
        # 获取下载的文件名称
        if not len(title) > 0:
            title = str(uuid.uuid1()) + ".mp4"
        else:
            title = title + ".mp4"
        info_down_path = path + "/" + title

        if not os.path.exists(info_down_path):
            print("开始下载:{}".format(title))
            # print("名称:{}=================下载地址:{}".format(title, info_down_path))
            m3u8_html = item["m3u8_html"]
            # command = 'm3_dl {} -o {} -t6'.format(m3u8_html, info_down_path)
            # os.system(command)
            command = '{} -o={} -t=6'.format(m3u8_html, info_down_path)
            parser = m3_dl.createParse()
            # 运行下载
            m3_dl.main(parser.parse_args(command.split()))
            endtime_wm = time.time()
            # 执行时间
            exec_times = (datetime.datetime.fromtimestamp(endtime_wm) - datetime.datetime.fromtimestamp(
                starttime_wm)).seconds / 60
            print("{}的下载时间->".format(title), exec_times, "分")
        else:
            print(title + "====================>>>>已存在")


# 判断你是否开启线程
def thread_download(self, item):
    global pool1
    pool1.apply(self.go_thread_download, (item,))


# CPU核心线程数
cpu_count = multiprocessing.cpu_count()
print("CPU核心线程数", cpu_count)
# 开启进程池
pool1 = Pool(processes=cpu_count)


# pool1 = Pool(1)


class MienavDownloadPipeline(object):

    def process_item(self, item, spider):
        title = "".join(re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+', item['title'][0], re.S))
        info_os = check_os()
        if "Windows" == info_os:
            path = WIN_DOWNLOAD_PATH
        elif "macOS" == info_os:
            path = MAC_DOWNLOAD_PATH
        else:
            print("暂未识别系统无法下载内容")
            return item
        # 下载本地目录
        item["file_path"] = path
        # 判断文件夹是否存在 不存在直接makedirs 创建多级目录
        if not os.path.exists(path):
            os.makedirs(path)
        # 获取下载的文件名称
        if not len(title) > 0:
            title = str(uuid.uuid1()) + ".mp4"
        else:
            title = title + ".mp4"
        info_down_path = path + "/" + title

        if not os.path.exists(info_down_path):
            pool1.apply_async(go_thread_download, (item,))
            time.sleep(150)
        return item
