# -*- coding: utf-8 -*-
import multiprocessing

from scrapy import cmdline

from multiprocessing import Process
cpu_count = multiprocessing.cpu_count()
print("CPU核心线程数", cpu_count)
# 开启进程池
'''
自定义主入口
启动脚本
'''
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings



if __name__ == '__main__':
     process = CrawlerProcess(get_project_settings())
     cmdline.execute('scrapy crawl yellow_spiders --nolog '.split())
     # process.crawl('mienav_spiders')
     # process.crawl('test')
     # process.start()




