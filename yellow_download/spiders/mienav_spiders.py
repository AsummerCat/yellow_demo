# -*- coding: utf-8 -*-
import urllib
import re
import scrapy
import json
import base64
# import urllib2

from yellow_download.items import MieNavDownloadItem


class MienavSpidersSpider(scrapy.Spider):
    name = 'mienav_spiders'
    allowed_domains = ['mienav.com']
    # 详细页
    # detail_url_prefix = "https://www.mienav.com{}"
    # 网站前缀
    index_url_prefix = "https://www.mienav.com{}"
    # 首页
    index_url = "https://www.mienav.com/index.php/vod/type/id/106.html"
    # 列表页
    url_prefix = index_url + "/page/{}.html"
    start_urls = [index_url]

    # 获取第一页数据及其所有列表
    def parse(self, response):

        index_list = response.xpath(
            "//div[@class='group-contents layui-row']/a[@class='group-item layui-col-md3 m-md6']")
        for i in index_list:
            # 遍历节点
            data = MieNavDownloadItem()
            data['title'] = i.xpath("p/text()").extract()
            data['url'] = self.index_url_prefix.format(i.attrib.get("href"))
            # print(data['title'], data['url'])
            yield scrapy.Request(data['url'], callback=self.get_detail_ver_html,
                                 meta={"item": data})

            # 获取最大页数
        max_page_html = response.xpath(
            "//div[@class='group-contents layui-row']/div[@class='page_wrap']/div/ul/li[last()]/a/@href").extract_first()[
                        -10:-1]
        max_page = re.sub("\D", "", max_page_html)
        # 最大页数存在
        if max_page:
            for i in range(2, int(max_page) + 1):
                next_url = self.url_prefix.format(str(i))
                # yield scrapy.Request(next_url, callback=self.next_parse)

    # # 下一页
    def next_parse(self, response):
        index_list = response.xpath(
            "//div[@class='group-contents layui-row']/a[@class='group-item layui-col-md3 m-md6']")
        for i in index_list:
            # 遍历节点
            data = MieNavDownloadItem()
            data['title'] = i.xpath("p/text()").extract()
            data['url'] = i.attrib.get("href")
            yield scrapy.Request(self.index_url_prefix.format(data['url']), callback=self.get_detail_ver_html,
                                 meta={"item": data})

    # 获取详情页的数据
    def get_detail_ver_html(self, response):
        data = response.meta["item"]
        detail_ver_html = response.xpath("/html/body/div[1]/div[3]/div/a/@href").extract_first()
        data["detail_vcr_html"] = self.index_url_prefix.format(detail_ver_html)
        yield scrapy.Request(data["detail_vcr_html"], callback=self.detail_pares, meta={"item": data})

    # 获取播放页的下载地址
    def detail_pares(self, response):
        data = response.meta["item"]
        # 获取网页原文
        detail_info = response.body_as_unicode()
        # 获取需要的json字符串
        json_string = detail_info.split("var player_data=")[1].split("</script>")[0]
        # json字符串转换dict
        json_obj = json.loads(json_string)
        # 获取出加密的m3u8_url
        m3u8_url = json_obj['url']
        # base64解密
        m3u8_base64decode_url = base64.b64decode(m3u8_url).decode("utf-8")

        # escape解密 获取解密后的m3u8_url
        m3u8_url = urllib.parse.unquote(m3u8_base64decode_url.encode().decode('unicode-escape'))
        data["m3u8_html"] = m3u8_url
        # 完整路径
        # https://www.mienav.com/addons/dplayer/?url=https://qiyiquotv.com/20200704/AJLVnsqL/index.m3u8
        yield data
