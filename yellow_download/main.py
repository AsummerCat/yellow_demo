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

if __name__ == '__main__':
    cmdline.execute('scrapy crawl yellow_spiders --nolog '.split())
