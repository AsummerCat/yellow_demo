# -*- coding: utf-8 -*-
import urllib

import scrapy

from yellow_download.items import YellowDownloadItem


class YellowSpidersSpider(scrapy.Spider):
    name = 'yellow_spiders'
    allowed_domains = ['mm006.xyz']
    # 搜索的内容
    key=urllib.parse.quote("漂亮女神")
    # key = '%E6%A0%A1%E8%8A%B1'
    # 详细页
    detail_url_prefix = "https://mm006.xyz{}"
    # 列表页
    url_prefix = "https://mm006.xyz/search.php?key={}&type=".format(key)

    start_urls = [url_prefix + '1']

    # 获取第一页数据及其所有列表
    def parse(self, response):
        index_list = response.xpath("//div[@class='item']")
        for i in index_list:
            # 遍历节点
            data = YellowDownloadItem()
            data['title'] = i.xpath(".//a[@class='movie-box']/div[@class='photo-info']/span/text()").extract()[0]
            data['url'] = i.xpath("./a[@class='movie-box']/@href").extract_first()
            yield scrapy.Request(self.detail_url_prefix.format(data['url']), callback=self.detail_pares,
                                 meta={"item": data})

            # 获取最大页数
        max_page = response.xpath("//div[@class='text-center']/ul/li/a[@class='end']/text()").extract_first()
        # 最大页数存在
        if max_page:
            for i in range(2, int(max_page) + 1):
                next_url = self.url_prefix + str(i)
                yield scrapy.Request(next_url, callback=self.next_parse)

    # 下一页
    def next_parse(self, response):
        index_list = response.xpath("//div[@class='item']")
        for i in index_list:
            # 遍历节点
            data = YellowDownloadItem()
            data['title'] = i.xpath(".//a[@class='movie-box']/div[@class='photo-info']/span/text()").extract()[0]
            data['url'] = i.xpath("./a[@class='movie-box']/@href").extract_first()
            yield scrapy.Request(self.detail_url_prefix.format(data['url']), callback=self.detail_pares,
                                 meta={"item": data})

    # 获取详情页的数据
    def detail_pares(self, response):
        data = response.meta["item"]
        my_video = response.xpath("//source")
        data["down_path"] = my_video[1].xpath("./@src").extract_first()
        yield data

# url='https://mm006.xyz/v.php?v=MjQyNzE1NDkvc2x1dHR5X2JydW5ldHRlX2JhYmVfaGFzX2FfZnVja190aGF0X2xlYXZlc19oZXJfb3JnYXNtaWM='
