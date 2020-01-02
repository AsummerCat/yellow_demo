# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

'''
管道下载
'''
import json
import os
import platform
import re
import uuid

import requests
from pyaria2 import Aria2RPC


class YellowDownloadPipeline(object):
    def process_item(self, item, spider):
        title = "".join(re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+', item['title'], re.S))
        # path = 'E:\\测试下载'
        path = '/Users/cat/Downloads'
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
