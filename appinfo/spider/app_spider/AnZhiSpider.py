from spider.app_spider.request_compoent import RqCompoent
from spider.app_spider.ParseCompoent import ParseComponent
from lxml import etree
import re


class AnZhiSpider(ParseComponent):
    def __init__(self, keyword):
        super(AnZhiSpider, self).__init__("http://www.anzhi.com/search.php?keyword=", keyword)
        self.url = "http://www.anzhi.com/search.php?keyword=" + self.quote_keyword
        self.n_page = 2
        self.name = "安智市场"

    def get_app_list_elements(self, url) -> list:
        response = RqCompoent.get(url)
        selector = etree.HTML(response)
        lis = selector.xpath("//div[@class='app_list border_three']/ul//li")
        return lis

    def get_page_n_url(self, n):
        if n == 1:
            return self.url
        page_n_url = self.url + "&page={}".format(n)
        return page_n_url

    def get_app_name(self, li):
        app_name = li.xpath("div[@class='app_info']/span[@class='app_name']/a/text()")
        return app_name

    def get_update_time(self, inner_response):
        pat_update_time = '时间：(.*?)</li>'
        update_time = re.findall(pat_update_time, inner_response)
        return update_time

    def get_author(self, inner_response):
        """获取发行商"""
        author_pat = '作者：(.*?)</li>'
        author = re.findall(author_pat, inner_response)
        return author

    def get_download_url(self, inner_response):
        """获取下载地址"""
        app_id_pat = 'opendown\((.*?)\);" title="下载到电脑"'
        app_id = re.findall(app_id_pat, inner_response)
        if app_id:
            app_id = app_id[0]
        download_url = "http://www.anzhi.com/dl_app.php?s=" + app_id + "&n=5"
        return download_url

    def get_enter_url(self, li):
        enter_url = li.xpath("div[@class='app_info']/span[@class='app_name']/a/@href")
        enter_url = self.judge_null(enter_url)
        enter_url = "http://www.anzhi.com" + enter_url
        return enter_url

    def get_version(self, inner_response):
        pat_version = '<span class="app_detail_version">\((.*?)\)</span>'
        version_num = re.findall(pat_version, inner_response)
        return version_num

    def get_img_address(self, li):
        selector = etree.HTML(self.inner_response)
        img_address = selector.xpath('//div[@class="detail_icon"]/img/@src')
        img_address = self.judge_null(img_address)
        img_address = "http://www.anzhi.com/" + img_address
        return img_address

    def get_app_intro(self, inner_response):
        selector = etree.HTML(self.inner_response)
        app_intro = selector.xpath('//div[@class="app_detail_infor"]/p/text()')
        app_intro = self.judge_null(app_intro)
        if isinstance(app_intro, str):
            app_intro = app_intro.strip()
        return app_intro


if __name__ == '__main__':
    anzhi_spider = AnZhiSpider(keyword="国信证券")
    anzhi_spider.parse()
