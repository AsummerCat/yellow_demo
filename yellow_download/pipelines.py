# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

'''
管道下载
'''
import os
import re
import time
import uuid
from pyaria2 import Aria2RPC


class YellowDownloadPipeline(object):
    def process_item(self, item, spider):
        title = "".join(re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+', item['title'], re.S))
        path = 'E:\\测试下载'
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
        info_down_path = path + "\\" + title

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
        self.get_file_from_url(path, down_path, title)

    # 根据文件链接+文件名称 添加下载任务
    def get_file_from_url(self, path, link, file_name):
        # 延时60s加载下一个
        time.sleep(60)
        jsonrpc = Aria2RPC()
        options = {"dir": path, "out": file_name, }
        res = jsonrpc.addUri([link], options=options)
