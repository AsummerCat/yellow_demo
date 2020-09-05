# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

'''
结构定义

'''


class YellowDownloadItem(scrapy.Item):
    # define the fields for your item here like:
    # 标题
    title = scrapy.Field()
    # 列表地址
    url = scrapy.Field()
    # 视频下载地址
    down_path = scrapy.Field()
    # 下载电脑的地址
    info_down_path = scrapy.Field()
    # 下载本地目录
    file_path = scrapy.Field()


class MieNavDownloadItem(scrapy.Item):
    # define the fields for your item here like:
    # 标题
    title = scrapy.Field()
    # 列表地址
    url = scrapy.Field()
    # 视频下载地址
    down_path = scrapy.Field()
    # 下载电脑的地址
    info_down_path = scrapy.Field()
    # 下载本地目录
    file_path = scrapy.Field()
    # 明细页的视频地址
    detail_vcr_html = scrapy.Field()
    # m3u8地址
    m3u8_html = scrapy.Field()
