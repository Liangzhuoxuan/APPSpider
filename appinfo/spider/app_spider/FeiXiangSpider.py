from spider.app_spider.request_compoent import RqCompoent
from spider.app_spider.ParseCompoent import ParseComponent
from lxml import etree
import re
from urllib.parse import quote


class FeiXiangSpider(ParseComponent):
    def __init__(self, keyword):
        super(FeiXiangSpider, self).__init__("https://www.52z.com/search?keyword=&s=1001&page=1&ajax=1", keyword)
        quote_keyword = quote(keyword, encoding="gbk")
        self.url = "https://www.52z.com/search?keyword={}&s=1001&page=1&ajax=1".format(quote_keyword)
        self.name = "飞翔下载"

    def get_app_list_elements(self, url="https://www.52z.com/search?keyword=&s=1001&page=1&ajax=1") -> list:
        print(self.url)
        response = RqCompoent.get(self.url)
        
        # self.outer_response = response
        selector = etree.HTML(response)
        lis = selector.xpath("body//li")
        # print(lis)
        return lis

    def get_page_n_url(self, n=2):
        if n == 1:
            return self.url
        page_n_url = self.url.replace("page=1", "page={}".format(n))
        return page_n_url

    def get_app_name(self, li):
        app_name = li.xpath("string(dl/dt//a)")
        print(app_name)
        version_string = li.xpath("dl/dt/p/text()")
        if version_string:
            version_string = version_string[0]
        vv = version_string.split()
        if len(vv) == 2:
            version = vv[0]
        else:
            version = None
        self.vv = version
        # app_name = re.findall('<div class="app-detail"><h4><a href=".*?">(.*?)</a></h4>', self.outer_response, re.S)
        # if '(' in app_name:
        #     app_name = app_name.split('(')[0]
        # app_name = [app_name]
        return [app_name]

    def get_update_time(self, inner_response):
        pat_update_time = '<li>更新时间：<span>(.*?)</span></li>'
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
        another_response = RqCompoent.get("https://www.52z.com/soft/downview?id=" + self.app_id)
        download_pat = 'http://(.*?)\.apk'
        download_url = re.findall(download_pat, another_response, re.S)
        if download_url:
            download_url = download_url[0]
            download_url = "http://" + download_url[0] + ".apk"
        else:
            download_url = []
        # selector = etree.HTML(inner_response)
        # download_url = selector.xpath("/html/body[@id='body']/div[@class='elywNei']/div[@class='elRight']/div[@class='elYxjsBox'][3]/div[@id='downajaxview']/div[@class='elYxxzIn'][1]/ul[@class='elYxxzList']/li[1]/a/@href")
        # download_url = self.judge_null(download_url)
        return download_url

    def get_enter_url(self, li):
        enter_url = li.xpath("dl/dt/a/@href")
        # enter_url = re.findall('<div class="app-detail"><h4><a href="(.*?)">.*?</a></h4>', self.outer_response, re.S)
        enter_url = self.judge_null(enter_url)
        # try:
        enter_url = "https://www.52z.com" + enter_url
        self.app_id = enter_url.split('/')[-1].split('.')[0]
        # print("self.app_id", self.app_id)
        return enter_url

    def get_version(self, inner_response):
        # pat_version = '<li>更新时间：<span>(.*?)</span></li>'
        # 这里为什么 <br> 不行，因为他会自动被解析为 \n 
        # version_num = re.findall(pat_version, inner_response, re.S)
        version = self.vv
        return version

    def get_img_address(self, li):
        selector = etree.HTML(self.inner_response)
        img_address = selector.xpath('//div[@class="elXxLeft"]/dl/dt/img/@src')
        img_address = self.judge_null(img_address)
        # img_address = "http://www.anzhi.com/" + img_address
        return img_address

    def get_app_intro(self, inner_response):
        selector = etree.HTML(self.inner_response)
        app_intro = selector.xpath('//div[@class="elYxjsCont contentBox"]/p/span/text()')
        app_intro = self.judge_null(app_intro)
        if isinstance(app_intro, str):
            app_intro = app_intro.strip()
        return app_intro

if __name__ == '__main__':
    feixiang_spider = FeiXiangSpider(keyword="支付")
    feixiang_spider.parse()
    # import urllib
    # urllib.parse.quote()
