from spider.app_spider.request_compoent import RqCompoent
from spider.app_spider.ParseCompoent import ParseComponent
from lxml import etree
import re


# TODO 有一个bug不知道咋整，就是 1解析出 2、3解析不出，4解析出， 5、6解析不出
class AnBeiSpider(ParseComponent):
    def __init__(self, keyword):
        super(AnBeiSpider, self).__init__("http://zhiyingyong.com/search", keyword)
        self.url = "http://zhiyingyong.com/search"
        self.name = "安贝市场"

    def get_app_list_elements(self, url="http://zhiyingyong.com/search") -> list:
        response = RqCompoent.post(url, {"apptitle":self.keyword}, {"Referer":"http://zhiyingyong.com"})
        self.outer_response = response
        # print(response)
        selector = etree.HTML(response)
        lis = selector.xpath("//div[@class='content-categoryCtn']/div[@class='content-categoryCtn-content clearfix']//div[@class='app-max']")
        # print(lis)
        return lis

    def get_page_n_url(self, n=2):
        # 因为小米这个的话，一页是很多个 app 的，没必要翻页
        if n == 1:
            return self.url
        page_n_url = self.url + "&page={}".format(n)
        return page_n_url

    def get_app_name(self, li):
        app_name = li.xpath("div[2]/h4/a/text()")
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
        enter_url = li.xpath("div[2]/h4/a/@href")
        # enter_url = re.findall('<div class="app-detail"><h4><a href="(.*?)">.*?</a></h4>', self.outer_response, re.S)
        enter_url = self.judge_null(enter_url)
        # try:
        enter_url = "http://zhiyingyong.com" + enter_url
        # except:
        #     enter_url = "http://zhiyingyong.com"
        return enter_url

    def get_version(self, inner_response):
        pat_version = '版本号：</span><div.*?>(.*?)</div></li>'
        # 这里为什么 <br> 不行，因为他会自动被解析为 \n 
        version_num = re.findall(pat_version, inner_response, re.S)
        return version_num

    def get_img_address(self, li):
        selector = etree.HTML(self.inner_response)
        img_address = selector.xpath('//div[@class="content-detailCtn-icon"]/p/img/@src')
        img_address = self.judge_null(img_address)
        # img_address = "http://www.anzhi.com/" + img_address
        return img_address

    def get_app_intro(self, inner_response):
        selector = etree.HTML(self.inner_response)
        app_intro = selector.xpath('//div[@class="content-detailCtn-text"]/div/div/text()')
        app_intro = self.judge_null(app_intro)
        if isinstance(app_intro, str):
            app_intro = app_intro.strip()
        return app_intro

if __name__ == '__main__':
    liqu_spider = AnBeiSpider(keyword="支付")
    liqu_spider.parse()
