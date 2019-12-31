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
import uuid


class YellowDownloadPipeline(object):
    def process_item(self, item, spider):
        title = "".join(re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+', item['title'], re.S))
        path = 'E:\\测试下载'
        # 判断文件夹是否存在 不存在直接makedirs 创建多级目录
        if not os.path.exists(path):
            os.makedirs(path)
            # 获取下载的文件名称
        if not len(title) > 0:
            title = str(uuid.uuid1())
        item["info_down_path"] = path + "\\" + title + ".mp4"
        return item
        print("开始下载:{}".format(title))

        # print("名称:{}=================下载地址:{}".format(title, item["down_path"]))
        # return item
