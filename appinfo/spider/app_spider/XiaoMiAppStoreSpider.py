from spider.app_spider.request_compoent import RqCompoent
from spider.app_spider.ParseCompoent import ParseComponent
from lxml import etree
import re


class XiaoMiAppStoreSpider(ParseComponent):
    def __init__(self, keyword):
        super(XiaoMiAppStoreSpider, self).__init__("http://app.mi.com/searchAll?keywords=&typeall=phone", keyword)
        self.url = "http://app.mi.com/searchAll?keywords={}&typeall=phone".format(self.quote_keyword)
        self.name = "小米应用市场"
        self.n_page = 1

    def get_app_list_elements(self, url) -> list:
        response = RqCompoent.get(url)
        selector = etree.HTML(response)
        lis = selector.xpath("//div[@class='main-con']/div[@class='applist-wrap']/ul[@class='applist']//li")
        return lis

    def get_page_n_url(self, n=1):
        # 因为小米这个的话，一页是很多个 app 的，没必要翻页
        if n == 1:
            return self.url
        page_n_url = self.url + "&page={}".format(n)
        return page_n_url

    def get_app_name(self, li):
        app_name = li.xpath("h5/a/text()")
        return app_name

    def get_update_time(self, inner_response):
        pat_update_time = '<li class="weight-font">更新时间：</li><li>(.*?)</li>'
        update_time = re.findall(pat_update_time, inner_response)
        return update_time

    def get_author(self, inner_response):
        """获取发行商"""
        author_pat = '<div class="intro-titles"><p>(.*?)</p>'
        author = re.findall(author_pat, inner_response)
        return author

    def get_download_url(self, inner_response):
        """获取下载地址"""
        download_pat = '<div class="app-info-down"><a href="(.*?)" class="download">直接下载</a>'
        download_url = re.findall(download_pat, inner_response, re.S)
        # selector = etree.HTML(inner_response)
        # download_url = selector.xpath("/html/body/div[@id='doc']/div[@class='yui3-g']/div[@class='yui3-u content-main']/div[@class='app-intro']/div[@class='intro-top']/div[@class='area-one-setup']/span[@class='one-setup-btn']/@data_url")
        download_url = self.judge_null(download_url)
        if isinstance(download_url, str):
            download_url = "http://app.mi.com" + download_url
        else:
            download_url = None
        return download_url

    def get_enter_url(self, li):
        enter_url = li.xpath("h5/a/@href")
        enter_url = self.judge_null(enter_url)
        enter_url = "http://app.mi.com" + enter_url
        return enter_url

    def get_version(self, inner_response):
        pat_version = '<li class="weight-font">版本号：</li><li>(.*?)</li>'
        version_num = re.findall(pat_version, inner_response)
        return version_num

    def get_img_address(self, li):
        selector = etree.HTML(self.inner_response)
        img_address = selector.xpath('//div[@class="app-intro cf"]/div[@class="app-info"]/img/@src')
        img_address = self.judge_null(img_address)
        return img_address

    def get_app_intro(self, inner_response):
        selector = etree.HTML(self.inner_response)
        app_intro = selector.xpath('//div[@class="app-text"]/p[1]/text()')
        app_intro = self.judge_null(app_intro)
        if isinstance(app_intro, str):
            app_intro = app_intro.strip()
        return app_intro

if __name__ == '__main__':
    xiaomi_spider = XiaoMiAppStoreSpider(keyword="支付")
    xiaomi_spider.parse()
