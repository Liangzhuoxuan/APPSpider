from spider.app_spider.request_compoent import RqCompoent
from spider.app_spider.ParseCompoent import ParseComponent
from lxml import etree
import re
from time import sleep


class LvSeZiYuanWangSpider(ParseComponent):
    def __init__(self, keyword):
        super(LvSeZiYuanWangSpider, self).__init__("", keyword)
        self.url = "http://s.downcc.com/search/pc/{}_all_hits.html".format(self.quote_keyword)
        self.n_page = 2
        self.name = "绿色资源网"

    def get_app_list_elements(self, url) -> list:
        response = RqCompoent.get(url)
        self.outer_response = response
        selector = etree.HTML(response)
        lis = selector.xpath('//div[@class="m-solist"]//div')
        # print(lis)
        return lis

    def get_page_n_url(self, n=1):
        if n == 1:
            return self.url
        # https://s.pc6.com/?f=2&k=%E6%94%AF%E4%BB%98
        page_n_url = self.url.replace("?k=", "?f={}&k=".format(n))
        return page_n_url

    # def loop_request(self, lis, first_page=True, **kwargs):
    #     """循环请求"""
    #     for li in lis:
    #         if not li[1].xpath("div/p[@class='info']"):
    #             continue
    #         app_name = self.get_app_name(li)
    #         app_name = self.judge_null(app_name)
    #         app_name = self.field_strip(app_name)
    #         enter_url = self.get_enter_url(li)  # 获取详情页url
    #         inner_response = RqCompoent.get(enter_url, **self.add_headers)
    #         fields = self.parse_app_info_page(inner_response)
    #         to_sink = [app_name, *fields]
    #         print(*to_sink)
    #         sleep(self.delay_time)

    def get_app_name(self, li):
        app_name = li.xpath("string(dl[1]/dt//a)")
        try:
            app_name, self.app_version = app_name.split('v')
        except:
            app_name, self.app_version = app_name.split('V')
        # app_name = re.findall('<div class="app-detail"><h4><a href=".*?">(.*?)</a></h4>', self.outer_response, re.S)
        # if '(' in app_name:
        #     app_name = app_name.split('(')[0]
        # app_name = [app_name]
        # print(app_name)
        return [app_name]

    def get_update_time(self, inner_response):
        pat_update_time = '更新时间：(.*?)<'
        update_time = re.findall(pat_update_time, inner_response)
        return update_time

    def get_author(self, inner_response):
        """获取发行商"""
        # author_pat = '作者：<s title=".*?">(.*?)<'
        # author = re.findall(author_pat, inner_response)
        # a = self.judge_null(author)
        return None

    def get_download_url(self, inner_response):
        """获取下载地址"""
        # download_pat = '<a id="address" href="(.*?)".*?>立即下载</a>'
        # download_url = re.findall(download_pat, inner_response, re.S)
        selector = etree.HTML(inner_response)
        download_url = selector.xpath(
            "//section[@class='border mod-hd-border-cl soft-details']/article[@class='w-360 fl-lf']/div[@class='maindown_w4']/a/@href")
        download_url = self.judge_null(download_url)
        return download_url

    def get_enter_url(self, li):
        enter_url = li.xpath("dl[2]/dd/a/@href")
        enter_url = self.judge_null(enter_url)
        # app_id = re.findall("([0-9]+)\.html", enter_url)
        # self.app_id = self.judge_null(app_id)
        return enter_url

    def get_version(self, inner_response):
        # pat_version = '版本：(.*?)<'
        # 这里为什么 <br> 不行，因为他会自动被解析为 \n 
        # version_num = re.findall(pat_version, inner_response, re.S)
        return [self.app_version]

    def get_img_address(self, li):
        selector = etree.HTML(self.inner_response)
        img_address = selector.xpath('//header[@class="mod-hd soft-titlebg"]/h1/em/img/@src')
        img_address = self.judge_null(img_address)
        # img_address = "http://www.anzhi.com/" + img_address
        return img_address

    def get_app_intro(self, inner_response):
        selector = etree.HTML(self.inner_response)
        app_intro = selector.xpath('string(//div[@class="soft-introduction-bd"]//p)')
        app_intro = self.judge_null(app_intro)
        if isinstance(app_intro, str):
            app_intro = app_intro.strip()
        return app_intro


if __name__ == '__main__':
    lvse_spider = LvSeZiYuanWangSpider(keyword="支付")
    lvse_spider.parse()
