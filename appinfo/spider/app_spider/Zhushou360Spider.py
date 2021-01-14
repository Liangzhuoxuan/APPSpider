from spider.app_spider.request_compoent import RqCompoent
from spider.app_spider.ParseCompoent import ParseComponent
from lxml import etree
import re


# 解析Json才行
class Zhushou360Spider(ParseComponent):
    def __init__(self, keyword):
        super(Zhushou360Spider, self).__init__("http://zhushou.360.cn/search/index/?kw=", keyword)
        self.url = "http://zhushou.360.cn/search/index/?kw={}&page=1".format(self.quote_keyword)
        self.name = "360手机助手"
        self.n_page = 2

    def get_app_list_elements(self, url) -> list:
        response = RqCompoent.get(url)
        # print(response)
        selector = etree.HTML(response)
        lis = selector.xpath("//div[@class='main']/div[@class='SeaCon']/ul//li")
        # print(lis)
        return lis

    def get_page_n_url(self, n):
        if n == 1:
            return self.url
        page_n_url = self.url.replace("&page=1", "&page={}".format(n))
        return page_n_url

    def get_app_name(self, li):
        app_name = li.xpath("dl/dd/h3/a/@title")
        # print(app_name)
        return app_name

    def get_update_time(self, inner_response):
        update_time = re.findall("<strong>更新时间：</strong>(.*?)</td>", inner_response, re.S)
        return update_time

    def get_author(self, inner_response):
        """获取发行商"""
        author = re.findall("<strong>作者：</strong>(.*?)</td>", inner_response, re.S)
        return author

    def get_download_url(self, inner_response):
        """获取下载地址"""
        selector = etree.HTML(inner_response)
        download_url = selector.xpath("//div[@class='product btn_type1']/dl[@class='clearfix']/dd/div[@class='product-btn-container']/a[2]/@href")
        # if app_id:
        #     app_id = app_id[0]
        # download_url = re.findall('href="(.*?)" data-sid.*?>下载apk包</a>', inner_response, re.S)
        download_url = self.judge_null(download_url)
        if isinstance(download_url, str):
            download_url = download_url.split("&url=")[1]
        else:
            download_url = None
        return download_url

    def get_enter_url(self, li):
        enter_url = li.xpath("dl/dd/h3/a/@href")
        enter_url = self.judge_null(enter_url)
        enter_url = "http://zhushou.360.cn" + enter_url
        return enter_url

    def get_version(self, inner_response):
        version = re.findall("<strong>版本：</strong>(.*?)<", inner_response, re.S)
        return version

    def get_img_address(self, li):
        selector = etree.HTML(self.inner_response)
        img_address = selector.xpath('//div[@class="product btn_type1"]/dl/dt/img/@src')
        img_address = self.judge_null(img_address)
        # img_address = "http://www.anzhi.com/" + img_address
        return img_address

    def get_app_intro(self, inner_response):
        selector = etree.HTML(self.inner_response)
        app_intro = selector.xpath("//div[@class='sdesc clearfix']/div[1]/text()")
        app_intro = self.judge_null(app_intro)
        if isinstance(app_intro, str):
            app_intro = app_intro.strip()
        return app_intro

if __name__ == '__main__':
    zhushou360_spider = Zhushou360Spider(keyword="支付")
    zhushou360_spider.parse()
