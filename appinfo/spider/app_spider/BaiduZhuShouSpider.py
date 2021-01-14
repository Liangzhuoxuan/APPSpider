from spider.app_spider.request_compoent import RqCompoent
from spider.app_spider.ParseCompoent import ParseComponent
from lxml import etree
import re


class BaiduZhuShouSpider(ParseComponent):
    def __init__(self, keyword):
        super(BaiduZhuShouSpider, self).__init__("", keyword)
        self.url = "https://shouji.baidu.com/s?wd={}&data_type=app&f=header_app%40input".format(self.quote_keyword)
        self.name = "百度手机助手"
        self.n_page = 1

    def get_app_list_elements(self, url) -> list:
        response = RqCompoent.get(url)
        selector = etree.HTML(response)
        lis = selector.xpath('//ul[@class="app-list"]//li')
        return lis

    def get_page_n_url(self, n=1):
        if n == 1:
            return self.url
        page_n_url = self.url + "&page={}".format(n)
        return page_n_url

    def get_app_name(self, li):
        app_name = li.xpath("div[@class='app']/div[@class='info']/div[@class='top']/a/text()")
        return app_name

    def get_update_time(self, inner_response):
        # pat_update_time = '时间：(.*?)</li>'
        # update_time = re.findall(pat_update_time, inner_response)
        return None

    def get_author(self, inner_response):
        """获取发行商"""
        # author_pat = '作者：(.*?)</li>'
        # author = re.findall(author_pat, inner_response)
        return None

    def get_download_url(self, inner_response):
        """获取下载地址"""
        # download_pat = 'data_type="apk" data_url="(.*?)" data_name='
        # download_url = re.findall(download_pat, inner_response, re.S)
        selector = etree.HTML(inner_response)
        download_url = selector.xpath("/html/body/div[@id='doc']/div[@class='yui3-g']/div[@class='yui3-u content-main']/div[@class='app-intro']/div[@class='intro-top']/div[@class='area-one-setup']/span[@class='one-setup-btn']/@data_url")
        download_url = self.judge_null(download_url)
        return download_url

    def get_enter_url(self, li):
        enter_url = li.xpath("div[@class='app']/div[@class='info']/div[@class='top']/a/@href")
        enter_url = self.judge_null(enter_url)
        enter_url = "https://shouji.baidu.com" + enter_url
        return enter_url

    def get_version(self, inner_response):
        pat_version = '<span class="version">版本: (.*?)</span>'
        version_num = re.findall(pat_version, inner_response)
        return version_num

    def get_img_address(self, li):
        selector = etree.HTML(self.inner_response)
        img_address = selector.xpath('//div[@class="intro-top"]/div[1]/div[1]/img/@src')
        img_address = self.judge_null(img_address)
        return img_address

    def get_app_intro(self, inner_response):
        selector = etree.HTML(self.inner_response)
        app_intro = selector.xpath('//div[@class="section-body"]/div/p/text()')
        app_intro = self.judge_null(app_intro)
        if isinstance(app_intro, str):
            app_intro = app_intro.strip()
        return app_intro

if __name__ == '__main__':
    baidu_spider = BaiduZhuShouSpider(keyword="支付")
    baidu_spider.parse()
