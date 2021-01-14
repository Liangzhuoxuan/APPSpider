from spider.app_spider.request_compoent import RqCompoent
from spider.app_spider.ParseCompoent import ParseComponent
from lxml import etree
import re


# TODO 有一个bug不知道咋整，就是 1解析出 2、3解析不出，4解析出， 5、6解析不出
class WoJi5577Spider(ParseComponent):
    def __init__(self, keyword):
        super(WoJi5577Spider, self).__init__("http://s.5577.com/search/d/_az_hits.html", keyword)
        self.url = "http://s.5577.com/search/d/{}_az_hits.html".format(self.quote_keyword)
        self.name = "5577我机网"

    def get_app_list_elements(self, url="http://s.5577.com") -> list:
        response = RqCompoent.get(self.url)
        self.outer_response = response
        selector = etree.HTML(response)
        lis = selector.xpath("//div[@class='g-left f-fl']//div[@class='m-cont-list']")
        print(lis)
        return lis

    def get_page_n_url(self, n=1):
        if n == 1:
            return self.url
        page_n_url = self.url + "&page={}".format(n)
        return page_n_url

    def get_app_name(self, li):
        app_name = li.xpath("dl[@class='g-dl-top']/dt/a/text()")
        # app_name = re.findall('<div class="app-detail"><h4><a href=".*?">(.*?)</a></h4>', self.outer_response, re.S)
        # if '(' in app_name:
        #     app_name = app_name.split('(')[0]
        # app_name = [app_name]
        return app_name

    def get_update_time(self, inner_response):
        pat_update_time = '更新时间：</i>(.*?)</li>'
        update_time = re.findall(pat_update_time, inner_response)
        return update_time

    def get_author(self, inner_response):
        """获取发行商"""
        # 这个软件商城只有部分大厂的发行商信息，比如支付宝，微信这些才有
        author_pat = '<span class="info_company">(.*?)</span>'
        author = re.findall(author_pat, inner_response)
        return author

    def get_download_url(self, inner_response):
        """获取下载地址"""
        download_pat = '<a id="address" href="(.*?)".*?>立即下载</a>'
        download_url = re.findall(download_pat, inner_response, re.S)
        selector = etree.HTML(inner_response)
        # download_url = selector.xpath("/html/body/div[@class='container clearfix']/div[@id='content']/div[@class='content-detailCtn']/div[@class='content-detailCtn-icon']/a/@href")
        download_url = self.judge_null(download_url)
        return download_url

    def get_enter_url(self, li):
        enter_url = li.xpath("dl[@class='g-dl-top']/dt/a/@href")
        # enter_url = re.findall('<div class="app-detail"><h4><a href="(.*?)">.*?</a></h4>', self.outer_response, re.S)
        enter_url = self.judge_null(enter_url)
        # try:
        # enter_url = "http://zhiyingyong.com" + enter_url
        # except:
        #     enter_url = "http://zhiyingyong.com"
        return enter_url

    def get_version(self, inner_response):
        # pat_version = ''
        # 这里为什么 <br> 不行，因为他会自动被解析为 \n 
        # version_num = re.findall(pat_version, inner_response, re.S)
        return None

    def get_img_address(self, li):
        selector = etree.HTML(self.inner_response)
        img_address = selector.xpath('//dl[@class="m-softinfo"]/dt/img/@src')
        img_address = self.judge_null(img_address)
        # img_address = "http://www.anzhi.com/" + img_address
        return img_address

    def get_app_intro(self, inner_response):
        selector = etree.HTML(self.inner_response)
        app_intro = selector.xpath('string(//div[@class="content"]/p[1])')
        app_intro = self.judge_null(app_intro)
        if isinstance(app_intro, str):
            app_intro = app_intro.strip()
        return app_intro


if __name__ == '__main__':
    woji_spider = WoJi5577Spider(keyword="支付")
    woji_spider.parse()
