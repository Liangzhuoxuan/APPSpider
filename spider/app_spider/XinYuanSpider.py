from spider.app_spider.request_compoent import RqCompoent
from spider.app_spider.ParseCompoent import ParseComponent
from lxml import etree
import re
from urllib.parse import quote


# TODO 有一个bug不知道咋整，就是 1解析出 2、3解析不出，4解析出， 5、6解析不出
class XinYuanSpider(ParseComponent):
    def __init__(self, keyword):
        super(XinYuanSpider, self).__init__("", keyword)
        self.quote_keyword = quote(keyword, encoding="GBK")
        self.url = "https://www.wishdown.com/search?type=0&keyword={}".format(self.quote_keyword)
        self.n_page = 1
        self.name = "心愿下载"

    def get_app_list_elements(self, url) -> list:
        response = RqCompoent.get(self.url)
        self.outer_response = response
        selector = etree.HTML(response)
        lis = selector.xpath("//div[@class='result_box']//dl")
        # print(lis)
        return lis

    def get_page_n_url(self, n=1):
        if n == 1:
            return self.url
        page_n_url = self.url + "&page={}".format(n)
        return page_n_url

    def get_app_name(self, li):
        app_name = li.xpath("string(dt/a)")
        # app_name = re.findall('<div class="app-detail"><h4><a href=".*?">(.*?)</a></h4>', self.outer_response, re.S)
        # if '(' in app_name:
        #     app_name = app_name.split('(')[0]
        # app_name = [app_name]
        return [app_name]

    def get_update_time(self, inner_response):
        # print(inner_response)
        pat_update_time = '时间：(.*?)<'
        update_time = re.findall(pat_update_time, inner_response)
        return update_time

    def get_author(self, inner_response):
        """获取发行商"""
        # 这个软件商城只有部分大厂的发行商信息，比如支付宝，微信这些才有
        # author_pat = '<span class="info_company">(.*?)</span>'
        # author = re.findall(author_pat, inner_response)
        return None

    def get_download_url(self, inner_response):
        """获取下载地址"""
        # download_pat = 'href="https://(.*?)apk"'
        # download_url = re.findall(download_pat, inner_response, re.S)
        # download_url = "https://" + download_url[0] + "apk"
        selector = etree.HTML(inner_response)
        download_url = selector.xpath("//div[@class='mobgame_down_box']/div[@class='img_box']/a[@class='mobgame_down_btn']/@href")
        # selector = etree.HTML(inner_response)
        # download_url = selector.xpath("/html/body/div[@class='container clearfix']/div[@id='content']/div[@class='content-detailCtn']/div[@class='content-detailCtn-icon']/a/@href")
        download_url = self.judge_null(download_url)
        return download_url

    def get_enter_url(self, li):
        enter_url = li.xpath("dt/a/@href")
        # enter_url = re.findall('<div class="app-detail"><h4><a href="(.*?)">.*?</a></h4>', self.outer_response, re.S)
        enter_url = self.judge_null(enter_url)
        # try:
        # enter_url = "http://zhiyingyong.com" + enter_url
        # except:
        #     enter_url = "http://zhiyingyong.com"
        enter_url = "https://www.wishdown.com/" + enter_url
        return enter_url

    def get_version(self, inner_response):
        # pat_version = ''
        # 这里为什么 <br> 不行，因为他会自动被解析为 \n 
        # version_num = re.findall(pat_version, inner_response, re.S)
        return None

    def get_img_address(self, li):
        selector = etree.HTML(self.inner_response)
        img_address = selector.xpath('//div[@class="img_box"]/a/img/@src')
        img_address = self.judge_null(img_address)
        # img_address = "http://www.anzhi.com/" + img_address
        return img_address

    def get_app_intro(self, inner_response):
        selector = etree.HTML(self.inner_response)
        app_intro = selector.xpath('string(//div[@class="xxy_Yxjs_Box"]//p)')
        app_intro = self.judge_null(app_intro)
        if isinstance(app_intro, str):
            app_intro = app_intro.strip()
        return app_intro


if __name__ == '__main__':
    xinyuan_spider = XinYuanSpider(keyword="金太阳")
    xinyuan_spider.parse()
