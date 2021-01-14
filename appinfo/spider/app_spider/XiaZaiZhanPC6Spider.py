from spider.app_spider.request_compoent import RqCompoent
from spider.app_spider.ParseCompoent import ParseComponent
from lxml import etree
import re
from urllib.parse import quote


# TODO 下载地址的加密的 js 没弄，下载地址没弄
class XiaZaiZhanPC6Spider(ParseComponent):
    def __init__(self, keyword):
        super(XiaZaiZhanPC6Spider, self).__init__("https://s.pc6.com/cse/search?s=12026392560237532321&entry=1&ie=gbk&q=", keyword)
        quote_keyword = quote(keyword, encoding="gbk")
        self.url = "https://s.pc6.com/cse/search?s=12026392560237532321&entry=1&ie=gbk&q={}".format(quote_keyword)
        self.name = "PC6下载站"

    def get_app_list_elements(self, url="https://s.pc6.com/cse/search?s=12026392560237532321&entry=1&ie=gbk&q=") -> list:
        print(self.url)
        response = RqCompoent.get(self.url)
        
        # self.outer_response = response
        selector = etree.HTML(response)
        lis = selector.xpath("body[@id='search']/div[@id='mbody']/div[@id='scont']/dl[@id='result']//dt")
        # print(lis)
        return lis

    def get_page_n_url(self, n=2):
        if n == 1:
            return self.url
        page_n_url = self.url.replace("page=1", "page={}".format(n))
        return page_n_url

    def get_app_name(self, li):
        app_name = li.xpath("string(a)")
        app_name = app_name.replace("下载", "").replace(' ', '').replace('\n', '')
        # print(app_name)
        # app_name = re.findall('<div class="app-detail"><h4><a href=".*?">(.*?)</a></h4>', self.outer_response, re.S)
        # if '(' in app_name:
        #     app_name = app_name.split('(')[0]
        # app_name = [app_name]
        return [app_name]

    def get_update_time(self, inner_response):
        pat_update_time = '<i>更新：(.*?)</i>'
        update_time = re.findall(pat_update_time, inner_response)
        return update_time

    def get_author(self, inner_response):
        """获取发行商"""
        # 这个软件商城只有部分大厂的发行商信息，比如支付宝，微信这些才有
        author_pat = '作者：<s.*?>(.*?)</s>'
        author = re.findall(author_pat, inner_response)
        return author

    def get_download_url(self, inner_response):
        """获取下载地址"""
        download_pat = 'http://(.*?)\.apk'
        download_url = re.findall(download_pat, inner_response, re.S)
        # selector = etree.HTML(inner_response)
        # download_url = selector.xpath("/html/body[@id='body']/div[@class='elywNei']/div[@class='elRight']/div[@class='elYxjsBox'][3]/div[@id='downajaxview']/div[@class='elYxxzIn'][1]/ul[@class='elYxxzList']/li[1]/a/@href")
        # download_url = self.judge_null(download_url)
        return None

    def get_enter_url(self, li):
        enter_url = li.xpath("a/@href")
        # enter_url = re.findall('<div class="app-detail"><h4><a href="(.*?)">.*?</a></h4>', self.outer_response, re.S)
        enter_url = self.judge_null(enter_url)
        # try:
        # enter_url = "https://www.52z.com" + enter_url
        return enter_url

    def get_version(self, inner_response):
        pat_version = '<i>版本：(.*?)</i>'
        # 这里为什么 <br> 不行，因为他会自动被解析为 \n 
        version_num = re.findall(pat_version, inner_response, re.S)
        return version_num

    def loop_request(self, lis, first_page=True, **kwargs):
        """循环请求"""
        # for li in lis:
        #     app_name = self.get_app_name(li)
        #     app_name = self.judge_null(app_name)
        #     app_name = self.field_strip(app_name)
        #     enter_url = self.get_enter_url(li)
        #     # 如果 enter_url 不是以 .html 结尾，不要
        #     if not enter_url.endswith(".html"):
        #         continue
        #     inner_response = RqCompoent.get(enter_url)
        #     fields = self.parse_app_info_page(inner_response)
        #     to_sink = [app_name, *fields]
        #     print(*to_sink)
        #     # sleep(self.delay_time)
        for li in lis:
            enter_url = self.get_enter_url(li)  # 获取详情页url
            if not enter_url.endswith(".html"):
                continue
            inner_response = RqCompoent.get(enter_url, **self.add_headers)
            if inner_response:
                self.inner_response = inner_response
                self.li = li

                app_name = self.get_app_name(li)
                app_name = self.judge_null(app_name)
                app_name = self.field_strip(app_name)

                img_address = self.get_img_address(li)
                app_intro = self.get_app_intro(inner_response)
                fields = self.parse_app_info_page(inner_response)
                to_sink = [self.name, app_name, *fields, img_address, app_intro]
                print(*to_sink[:-1], to_sink[-1][:20])

    def get_img_address(self, li):
        selector = etree.HTML(self.inner_response)
        img_address = selector.xpath('//p[@id="dico"]/img/@src')
        img_address = self.judge_null(img_address)
        # img_address = "http://www.anzhi.com/" + img_address
        return img_address

    def get_app_intro(self, inner_response):
        selector = etree.HTML(self.inner_response)
        app_intro = selector.xpath('string(//div[@class="intro-txt"]//p)')
        app_intro = self.judge_null(app_intro)
        if isinstance(app_intro, str):
            app_intro = app_intro.strip()
        return app_intro


if __name__ == '__main__':
    pc6_spider = XiaZaiZhanPC6Spider(keyword="支付")
    pc6_spider.parse()
    # import urllib
    # urllib.parse.quote()
