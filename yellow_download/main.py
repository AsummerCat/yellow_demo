# -*- coding: utf-8 -*-
from scrapy import cmdline

'''
自定义主入口
启动脚本
'''

if __name__ == '__main__':
    # cmdline.execute('scrapy crawl yellow_spiders'.split())
    cmdline.execute('scrapy crawl mienav_spiders'.split())


