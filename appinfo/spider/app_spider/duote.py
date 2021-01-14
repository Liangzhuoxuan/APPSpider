from request_compoent import RqCompoent
from ParseCompoent import ParseComponent
from lxml import etree
import re
from urllib.parse import quote


class DuoTeSpider(ParseComponent):
    def __init__(self, keyword):
        super(DuoTeSpider, self).__init__("", keyword)
        k = quote(keyword, encoding="GBK")
        self.url = "http://s.duote.com:8081/search/softindex/?keywords=" + k
        # self.n_page = 2

    def get_app_list_elements(self, url) -> list:
        response = RqCompoent.get(url)
        self.outer_response = response
        print(response)
        selector = etree.HTML(response)
        lis = selector.xpath("//div[@class='listWrapper']")
        print(lis)
        return lis

    def get_page_n_url(self, n):
        if n == 1:
            return self.url
        page_n_url = self.url + "&page={}".format(n)
        return page_n_url

    def get_app_name(self, li):
        app_name = li.xpath("string(div[@class='list']/dl[@class='result']/dt/a)")
        # app_name = re.findall('<div class="app-detail"><h4><a href=".*?">(.*?)</a></h4>', self.outer_response, re.S)
        # if '(' in app_name:
        #     app_name = app_name.split('(')[0]
        # app_name = [app_name]
        return app_name

    def get_update_time(self, inner_response):
        pat_update_time = '更新时间：</span><div>(.*?)</div></li>'
        update_time = re.findall(pat_update_time, inner_response)
        return update_time

    def get_author(self, inner_response):
        """获取发行商"""
        author_pat = '开发商：</span><div>(.*?)</div></li>'
        author = re.findall(author_pat, inner_response)
        return author

    def get_download_url(self, inner_response):
        """获取下载地址"""
        # download_pat = '<div class="app-info-down"><a href="(.*?)" class="download">直接下载</a>'
        # download_url = re.findall(download_pat, inner_response, re.S)
        selector = etree.HTML(inner_response)
        download_url = selector.xpath("/html/body/div[@class='container clearfix']/div[@id='content']/div[@class='content-detailCtn']/div[@class='content-detailCtn-icon']/a/@href")
        download_url = self.judge_null(download_url)
        return download_url

    def get_enter_url(self, li):
        enter_url = li.xpath("div[@class='list']/dl[@class='result']/dd/div/p[@class='addr']/span[@class='url']/text()")
        # enter_url = re.findall('<div class="app-detail"><h4><a href="(.*?)">.*?</a></h4>', self.outer_response, re.S)
        enter_url = self.judge_null(enter_url)
        print(enter_url)
        return enter_url

    def get_version(self, inner_response):
        pat_version = '版本号：</span><div class="">(.*?)</div></li>'
        # 这里为什么 <br> 不行，因为他会自动被解析为 \n 
        version_num = re.findall(pat_version, inner_response, re.S)
        return version_num


if __name__ == '__main__':
    duote_spider = DuoTeSpider(keyword="支付")
    duote_spider.parse()
