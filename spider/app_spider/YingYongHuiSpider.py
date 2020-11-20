# from lxml import etree
# import re
# import urllib
# from request_compoent import RqCompoent
# import time
#
#
# def _run(keyword):
#     # keyword = "国信证券开户"
#     url = f"http://www.appchina.com/sou/?keyword={urllib.parse.quote(keyword)}"
#     response = RqCompoent.get(url)
#     parse(response, keyword, url)
#
#
# def parse(response, keyword, url):
#     selector = etree.HTML(response)
#     lis = selector.xpath("//div[@class='main']/div[@id='left']/ul[@class='app-list']//li")
#     flag = 1
#     for li in lis:
#         app_name = li.xpath("div[@class='app-info']/h1[@class='app-name']/a/text()")
#         inner_link = li.xpath("a/@href")
#         if inner_link:
#             inner_link = inner_link[0]
#         if app_name:
#             app_name = app_name[0]
#         if app_name == keyword:
#             inner_response = RqCompoent.get("http://www.appchina.com/" + inner_link)
#             parse_second(inner_response)
#             flag = 0
#             break
#
#     if flag:
#         # 第一页
#         for li in lis:
#             app_name = li.xpath("div[@class='app-info']/h1[@class='app-name']/a/text()")
#
#             inner_link = li.xpath("a/@href")
#             if inner_link:
#                 inner_link = inner_link[0]
#             print(app_name, inner_link)
#             inner_response = RqCompoent.get("http://www.appchina.com/" + inner_link)
#             parse_second(inner_response, app_name)
#             time.sleep(0.1)
#         # 第二页
#         page_two_link = url + "&page=2"
#         page_two_response = RqCompoent.get(page_two_link)
#         _selector = etree.HTML(page_two_response)
#         _lis = _selector.xpath("//div[@class='main']/div[@id='left']/ul[@class='app-list']//li")
#         for li in _lis:
#             inner_link = li.xpath("a/@href")
#             app_name = li.xpath("div[@class='app-info']/h1[@class='app-name']/a/text()")
#             if inner_link:
#                 inner_link = inner_link[0]
#             print(app_name, inner_link)
#             inner_response = RqCompoent.get("http://www.appchina.com/" + inner_link)
#             parse_second(inner_response, app_name)
#             time.sleep(0.1)
#
#
# def parse_second(inner_response, app_name):
#     # app_name = re.findall('<img class="Content_Icon".*?title="(.*?)"', inner_response, re.S)
#     # print(app_name)
#     # if app_name:
#     #     app_name = app_name[0]
#     version_pat = '<p class="art-content">版本：(.*?)</p>'
#     version = re.findall(version_pat, inner_response, re.S)
#     if version:
#         version = version[0]
#     print(version)
#     time_pat = '<p class="art-content">更新：(.*?)</p>'
#     time = re.findall(time_pat, inner_response, re.S)
#     if time:
#         time = time[0]
#
#     download_link = re.findall('meta-page=.*?href="(.*?)">下载', inner_response, re.S)
#     if download_link:
#         download_link = download_link[0]
#     print(download_link)
#
#     author_pat = "开发者：.+?href.+?>(.*?)<"
#     author = re.findall(author_pat, inner_response, re.S)
#     if author:
#         author = author[0]
#     print(author)
#
#
# if __name__ == '__main__':
#     _run("宝")
from spider.app_spider.request_compoent import RqCompoent
from spider.app_spider.ParseCompoent import ParseComponent
from lxml import etree
import re


class YingYongHuiSpider(ParseComponent):
    def __init__(self, keyword):
        super(YingYongHuiSpider, self).__init__("", keyword)
        self.url = "http://www.appchina.com/sou/?keyword={}&page=1".format(self.quote_keyword)
        self.n_page = 2
        self.delay_time = 0.5
        self.name = "应用汇"

    def get_app_list_elements(self, url) -> list:
        response = RqCompoent.get(url)
        if not response:
            return None
        selector = etree.HTML(response)
        lis = selector.xpath("//div[@class='main']/div[@id='left']/ul[@class='app-list']//li")
        return lis

    def get_page_n_url(self, n):
        if n == 1:
            return self.url
        page_n_url = self.url.replace("&page=", "&page={}".format(n))
        return page_n_url

    def get_app_name(self, li):
        app_name = li.xpath("div[@class='app-info']/h1[@class='app-name']/a/text()")
        return app_name

    def get_update_time(self, inner_response):
        pat_update_time = '<p class="art-content">更新：(.*?)</p>'
        update_time = re.findall(pat_update_time, inner_response)
        return update_time

    def get_author(self, inner_response):
        """获取发行商"""
        author_pat = '开发者：.+?href.+?>(.*?)<'
        author = re.findall(author_pat, inner_response)
        return author

    def get_download_url(self, inner_response):
        """获取下载地址"""
        down_pat = 'meta-page=.*?href="(.*?)">下载'
        download_url = re.findall(down_pat, inner_response)
        # if app_id:
        #     app_id = app_id[0]
        # download_url = "http://www.anzhi.com/dl_app.php?s=" + app_id + "&n=5"
        download_url = self.judge_null(download_url)
        return download_url

    def get_enter_url(self, li):
        enter_url = li.xpath("a/@href")
        enter_url = self.judge_null(enter_url)
        enter_url = "http://www.appchina.com/" + enter_url
        return enter_url

    def get_version(self, inner_response):
        pat_version = '<p class="art-content">版本：(.*?)</p>'
        version_num = re.findall(pat_version, inner_response)
        return version_num

    def get_img_address(self, li):
        selector = etree.HTML(self.inner_response)
        img_address = selector.xpath('//div[@class="msg"]/img/@src')
        img_address = self.judge_null(img_address)
        return img_address

    def get_app_intro(self, inner_response):
        selector = etree.HTML(self.inner_response)
        app_intro = selector.xpath('string(//div[@class="main-info"]/p)')
        # app_intro = "".join(app_intro)
        # app_intro = self.judge_null(app_intro)
        if isinstance(app_intro, str):
            app_intro = app_intro.strip()
        return app_intro


if __name__ == '__main__':
    anzhi_spider = YingYongHuiSpider(keyword="支付")
    anzhi_spider.parse()