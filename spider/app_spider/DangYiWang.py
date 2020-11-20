from spider.app_spider.request_compoent import RqCompoent
from spider.app_spider.ParseCompoent import ParseComponent
from spider.app_spider.ParseComponentAjax import ParseComponentAjax
from lxml import etree
from urllib.parse import quote
import json
import re
import time
import demjson


class DangYiWangSpider(ParseComponentAjax):
    def __init__(self, keyword):
        super(DangYiWangSpider, self).__init__("", keyword)
        self.url = "http://s.downyi.com/ajax.asp?action=28&num=20&urlclass=search&locationclass=search&typeclass=0&stype=all&o=hits&p=1&keyword={}".format(quote(keyword))
        self.n_page = 2
        self.name = "当易网"

    def get_app_list_elements(self, url) -> list:
        response = RqCompoent.get(url)
        if not response:
            return [None, None, None, None]
        # big_dict = json.loads(response)
        big_dict = demjson.decode(response)
        items = list(zip(big_dict.get("SoftUrl"), big_dict.get("ResName"), \
            big_dict.get("ResVer"), big_dict.get("UpdateTime"), big_dict.get("SmallImg")))
        return items

    def get_page_n_url(self, n):
        if n == 1:
            return self.url
        page_n_url = self.url.replace("&p=1", "&p={}".format(n))
        return page_n_url

    def get_app_name(self, item):
        if not item:
            return None
        app_name = item[1]
        # app_name = self.judge_null(app_name)
        # app_name = ''.join(re.findall("[\u4E00-\u9FFF]+", app_name))
        return app_name

    def get_update_time(self, inner_response, item):
        # print(inner_response)
        # pat_update_time = '<label>更新时间：</label>(.*?)</td>'
        # update_time = re.findall(pat_update_time, inner_response)
        # selector = etree.HTML(inner_response)
        # update_time = selector.xpath("//div[@class='det-main-container']/div[@class='det-othinfo-container J_Mod']/div[@class='det-othinfo-data']/@data-apkPublishTime")
        # update_time = item.get("appDetail").get("authorName")
        # update_time = self.judge_null(update_time).strip()
        if not item:
            return None
        return item[3]

    def get_author(self, inner_response, item):
        """获取发行商"""
        author_pat = '应用厂商：<a href=".*?" target="_blank">(.*?)<'
        author = re.findall(author_pat, inner_response)
        # author = item.get("appDetail").get("authorName")
        author = self.judge_null(author)
        return author

    def get_download_url(self, inner_response, li):
        """获取下载地址"""
        # d_url_pat = 'href="http:(.*?)\.apk"'
        # d_url = re.findall(d_url_pat, inner_response)
        # download_url = self.judge_null(d_url)
        return None

    def get_enter_url(self, item):
        if not item:
            return None
        return item[0]

    def get_version(self, inner_response, item):
        """获取版本号"""    
        # version = re.findall("版本：(.*?)<", inner_response)
        # version = self.judge_null(version).strip()
        if not item:
            return None
        return item[2]

    def get_img_address(self, item):
        img_address = item[4]
        return img_address

    def get_app_intro(self, inner_response):
        selector = etree.HTML(inner_response)
        app_intro = selector.xpath("//div[@class='des']/p[1]/text()")
        app_intro = self.judge_null(app_intro)
        if isinstance(app_intro, str):
            app_intro = app_intro.strip()
        return app_intro

if __name__ == '__main__':
    dangyi_spider = DangYiWangSpider(keyword="支付")
    dangyi_spider.parse()
