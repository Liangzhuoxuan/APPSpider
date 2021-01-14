from spider.app_spider.request_compoent import RqCompoent
from spider.app_spider.ParseCompoent import ParseComponent
from lxml import etree
import re


class LiQvSpider(ParseComponent):
    def __init__(self, keyword):
        super(LiQvSpider, self).__init__("https://s.liqucn.com/s.php?words=", keyword)
        self.url = "https://s.liqucn.com/s.php?words={}".format(self.quote_keyword)
        self.name = "历趣"

    def get_app_list_elements(self, url="https://s.liqucn.com/s.php?words=") -> list:
        response = RqCompoent.get(self.url)
        selector = etree.HTML(response)
        lis = selector.xpath("//div[@class='sear_app']//dl")
        return lis

    def get_page_n_url(self, n=2):
        # 因为小米这个的话，一页是很多个 app 的，没必要翻页
        if n == 1:
            return self.url
        page_n_url = self.url + "&page={}".format(n)
        return page_n_url

    def get_app_name(self, li):
        app_name = li.xpath("string(dd/h3//a)")
        if '(' in app_name:
            app_name = app_name.split('(')[0]
        app_name = [app_name]
        return app_name

    def get_update_time(self, inner_response):
        pat_update_time = '更新：<em>(.*?)</em>'
        update_time = re.findall(pat_update_time, inner_response)
        return update_time

    def get_author(self, inner_response):
        """获取发行商"""
        author_pat = '开发商：<em>(.*?)</em>'
        author = re.findall(author_pat, inner_response)
        return author

    def get_download_url(self, inner_response):
        """获取下载地址"""
        # download_pat = '<div class="app-info-down"><a href="(.*?)" class="download">直接下载</a>'
        # download_url = re.findall(download_pat, inner_response, re.S)
        # selector = etree.HTML(inner_response)
        # download_url = selector.xpath("/html/body/div[@class='box'][2]/div[@class='main']/div[@class='info_box']/div[@class='info_download']/div[@class='apk_btn']/a/@href")
        download_url = "https://count.liqucn.com/d.php?id={}&urlos=android&from_type=web".format(self.temp_app_id)
        # download_url = self.judge_null(download_url)
        return download_url

    def get_enter_url(self, li):
        enter_url = li.xpath("dd/h3/a/@href")
        enter_url = self.judge_null(enter_url)
        # /rj/10070.shtml
        self.temp_app_id = enter_url.split('/')[-1].split('.')[0]
        return enter_url

    def get_version(self, inner_response):
        pat_version = '最新版本：(.*?)<'
        # 这里为什么 <br> 不行，因为他会自动被解析为 \n 
        version_num = re.findall(pat_version, inner_response, re.S)
        return version_num

    def get_img_address(self, item):
        # img_address = item[4]
        selector = etree.HTML(self.inner_response)
        img_address = selector.xpath('//div[@class="info_con"]/img/@src')
        img_address = self.judge_null(img_address)
        return img_address

    def get_app_intro(self, inner_response):
        selector = etree.HTML(inner_response)
        app_intro = selector.xpath('//div[@class="description-wrapper"]/div[2]/text()')
        app_intro = self.judge_null(app_intro)
        if isinstance(app_intro, str):
            app_intro = app_intro.strip()
        return app_intro

if __name__ == '__main__':
    liqu_spider = LiQvSpider(keyword="支付")
    liqu_spider.parse()
