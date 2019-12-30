# -*- coding: utf-8 -*-
import scrapy

from yellow_download.items import YellowDownloadItem


class YellowSpidersSpider(scrapy.Spider):
    name = 'yellow_spiders'
    allowed_domains = ['mm006.xyz']
    # 搜索的内容
    key = '%E6%A0%A1%E8%8A%B1'
    # 详细页
    detail_url_prefix = "https://mm006.xyz{}"
    # 列表页
    url_prefix = "https://mm006.xyz/search.php?key={}&type=".format(key)

    start_urls = [url_prefix + '1']

    # 获取所有列表
    def parse(self, response):
        index_list = response.xpath("//div[@class='item']")
        for i in index_list:
            # 遍历节点
            data = YellowDownloadItem()
            # data['title'] = i.xpath("./div[@class='photo-info']/span/text()").extract_first()
            data['url'] = i.xpath("./a[@class='movie-box']/@href").extract_first()
            # print(data['title'])
            # print(data['url'])
            yield scrapy.Request(self.detail_url_prefix.format(data['url']), callback=self.detail_pares,
                                 meta={"item": data})

            # 获取最大页数
        max_page = response.xpath("//div[@class='text-center']/ul/li/a[@class='end']/text()").extract_first()
        # # 最大页数存在
        # if max_page:
        #     for i in max_page:
        #         yield scrapy.Request(self.url_prefix + str(i), callback=self.next_parse)

    # 下一页
    def next_parse(self, response):
        index_list = response.xpath("//div[@class='item']")
        for i in index_list:
            # 遍历节点
            data = YellowDownloadItem()
            data['url'] = i.xpath("./a[@class='movie-box']/@href").extract_first()
        yield scrapy.Request(
            self.detail_url_prefix.format(data['url']), callback=self.detail_pares, meta={"item": data})

    # 获取详情页的数据
    def detail_pares(self, response):
        # print(response.text)
        data = response.meta["item"]
        my_video = response.xpath("//video[@id='my-video']")

        for item in my_video:
            print(my_video.xpath("./source/@src").extract_first())
        # data["down_path"] = response.xpath("//video[@id='my-video']/source[2]/@src").extract_first()
        # print(data["down_path"])
        # yield data



url='https://mm006.xyz/v.php?v=MjQyNzE1NDkvc2x1dHR5X2JydW5ldHRlX2JhYmVfaGFzX2FfZnVja190aGF0X2xlYXZlc19oZXJfb3JnYXNtaWM='