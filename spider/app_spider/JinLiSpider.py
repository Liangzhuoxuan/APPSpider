from spider.app_spider.request_compoent import RqCompoent
from spider.app_spider.ParseCompoent import ParseComponent
from spider.app_spider.ParseComponentAjax import ParseComponentAjax
from lxml import etree
from urllib.parse import quote
import json
import re
import time


class JinLiSpider(ParseComponentAjax):
    def __init__(self, keyword):
        super(JinLiSpider, self).__init__("http://m.anzhuoapk.com/mobile/soft/search/?ks=", keyword)
        self.url = "http://m.anzhuoapk.com/mobile/soft/search/?ks={}".format(quote(keyword))
        self.n_page = 1
        self.name = "金立软件商店"

    def get_app_list_elements(self, url) -> list:
        response = RqCompoent.post(self.url, data={})
        big_dict = json.loads(response)
        html = big_dict.get("html").replace("=/", "=")
        selector = etree.HTML(html)
        lis = selector.xpath("//div[@class='cp-box clearfix']")
        return lis

    def get_page_n_url(self, n):
        if n == 1:
            return self.url
        page_letters = ['', 'MTA=', 'MjA=', 'MzA=']
        page_n_url = "https://sj.qq.com/myapp/searchAjax.htm?kw={}&pns={}&sid=0".format(self.quote_keyword, page_letters[n-1])
        return page_n_url

    def get_app_name(self, li):
        app_name = li.xpath("div/div[2]/p[1]/text()")
        app_name = self.judge_null(app_name)
        return app_name

    def get_update_time(self, inner_response, item):
        # print(inner_response)
        pat_update_time = '更新时间：(.*?)</span>'
        update_time = re.findall(pat_update_time, inner_response)
        # selector = etree.HTML(inner_response)
        # update_time = selector.xpath("//div[@class='det-main-container']/div[@class='det-othinfo-container J_Mod']/div[@class='det-othinfo-data']/@data-apkPublishTime")
        # update_time = item.get("appDetail").get("authorName")
        update_time = self.judge_null(update_time)
        return update_time

    def get_author(self, inner_response, item):
        """获取发行商"""
        author_pat = '开发者：(.*?)</p>'
        author = re.findall(author_pat, inner_response)
        # author = item.get("appDetail").get("authorName")
        author = self.judge_null(author)
        return author

    def get_download_url(self, inner_response, li):
        """获取下载地址"""
        # app_id_pat = 'opendown\((.*?)\);" title="下载到电脑"'
        # app_id = re.findall(app_id_pat, inner_response)
        download_url = li.xpath("a/@apkurl")
        if download_url:
            download_url = download_url[0]
        download_url = "http://m.anzhuoapk.com" + download_url
        return download_url

    def get_enter_url(self, li):
        apkurl = li.xpath("a/@apkurl")
        if apkurl:
            apkurl = apkurl[0]
        else:
            apkurl = ""
        app_id = re.findall("&id=(.*?)&", apkurl)
        if app_id:
            app_id = app_id[0]
        else:
            app_id = ""
        enter_url = "http://m.anzhuoapk.com/mobile/soft/detail/" + app_id
        return enter_url

    def get_version(self, inner_response, item):
        """获取版本号"""
        version = re.findall("版本号：(.*?)</span>", inner_response)
        version = self.judge_null(version)
        return version

    def get_img_address(self, item):
        # img_address = item[4]
        selector = etree.HTML(self.inner_response)
        img_address = selector.xpath('//img[@class="cp-big-icon"]/@src')
        img_address = self.judge_null(img_address)
        return img_address

    def get_app_intro(self, inner_response):
        selector = etree.HTML(inner_response)
        app_intro = selector.xpath("//div[@id='js-intro-txt']/p/text()")
        app_intro = self.judge_null(app_intro)
        if isinstance(app_intro, str):
            app_intro = app_intro.strip()
        return app_intro

if __name__ == '__main__':
    jinli_spider = JinLiSpider(keyword="金太阳")
    jinli_spider.parse()
