# from lxml import etree
# import urllib
# import re
# from request_compoent import RqCompoent


# def _run(keyword):
#     # keyword = "国信证券开户"
#     url = "http://zhushou.2345.com/index.php?c=web&d=doSearch&so={}".format(urllib.parse.quote(keyword))
#     print(url)
#     response = RqCompoent.get(url)
#     parse(response, keyword, url)


# def parse(response, keyword, url):
#     selector = etree.HTML(response)
#     lis = selector.xpath("//ul[@class='MlistC']//li")
#     # 热门的应用会使用这个MlistD这个class
#     extra = selector.xpath("//ul[@class='MlistD']//li")
#     if extra:
#         lis.append(extra[0])
#     flag = 1
#     for li in lis:
#         app_name = li.xpath("div[@class='name']/a/text()")[0]
#         # 如果找到与关键字相同的
#         if app_name == keyword:
#             enter_url = li.xpath("div[@class='name']/a/@href")[0]
#             inner_response = RqCompoent.get(enter_url)
#             parse_second(inner_response)
#             flag = 0
#             break

#     # 没有找到与关键字相同的，把前两页抓下来
#     if flag:
#         # 把前两页弄下来
#         for li in lis:
#             app_name = li.xpath("div[@class='name']/a/text()")[0]
#             print(app_name)
#             # 如果找到与关键字相同的
#             enter_url = li.xpath("div[@class='name']/a/@href")[0]
#             inner_response = RqCompoent.get(enter_url)
#             parse_second(inner_response)

#         page_two_response = RqCompoent.get(url + "&p=2")
#         _selector = etree.HTML(page_two_response)
#         _lis = _selector.xpath("//ul[@class='MlistC']//li")
#         for li in _lis:
#             app_name = li.xpath("div[@class='name']/a/text()")[0]
#             print(app_name)
#             # 如果找到与关键字相同的
#             enter_url = li.xpath("div[@class='name']/a/@href")[0]
#             inner_response = RqCompoent.get(enter_url)
#             parse_second(inner_response)


# def parse_second(inner_response):
#     version_pat = '<span class="field">版本：</span>(.*?)</li>'
#     version = re.findall(version_pat, inner_response, re.S)
#     update_time_pat = '<span class="field">更新：</span>(.*?)</li>'
#     update_time = re.findall(update_time_pat, inner_response, re.S)
#     author_pat = '<span class="field">作者：</span>(.*?)</li>'
#     author = re.findall(author_pat, inner_response, re.S)
#     download_link_pat = '<a class="btn_down_to_pc" href="(.*?)" rel="nofollow">下载到电脑</a>'
#     download_link = re.findall(download_link_pat, inner_response, re.S)
#     if version:
#         version = version[0]
#     if update_time:
#         update_time = update_time[0]
#     if author:
#         author = author[0]
#     if download_link:
#         download_link = download_link[0]

#     print(version, update_time, author, download_link)


# if __name__ == '__main__':
#     _run("金太阳手机炒股")

from spider.app_spider.request_compoent import RqCompoent
from spider.app_spider.ParseCompoent import ParseComponent
from lxml import etree
import re


class ShouJiZhuShou2345Spider(ParseComponent):
    def __init__(self, keyword):
        super(ShouJiZhuShou2345Spider, self).__init__("", keyword)
        self.url = "http://zhushou.2345.com/index.php?c=web&d=doSearch&so={}&p=1".format(self.quote_keyword)
        self.n_page = 2
        self.name = "2345手机助手"

    def get_app_list_elements(self, url) -> list:
        response = RqCompoent.get(url)
        selector = etree.HTML(response)
        lis = selector.xpath("//ul[@class='MlistC']//li")
        extra = selector.xpath("//ul[@class='MlistD']//li")
        if extra:
            lis.append(extra[0])
        return lis

    def get_page_n_url(self, n):
        if n == 1:
            return self.url
        page_n_url = self.url.replace("&p=1", "&p={}".format(n))
        return page_n_url

    def get_app_name(self, li):
        app_name = li.xpath("div[@class='name']/a/text()")
        return app_name

    def get_update_time(self, inner_response):
        pat_update_time = '<span class="field">更新：</span>(.*?)</li>'
        update_time = re.findall(pat_update_time, inner_response)
        return update_time

    def get_author(self, inner_response):
        """获取发行商"""
        author_pat = '<span class="field">作者：</span>(.*?)</li>'
        author = re.findall(author_pat, inner_response)
        return author

    def get_download_url(self, inner_response):
        """获取下载地址"""
        down_pat = '<a class="btn_down_to_pc" href="(.*?)" rel="nofollow">下载到电脑</a>'
        download_url = re.findall(down_pat, inner_response)
        # if app_id:
        #     app_id = app_id[0]
        # download_url = "http://www.anzhi.com/dl_app.php?s=" + app_id + "&n=5"
        download_url = self.judge_null(download_url)
        return download_url
    
    def get_enter_url(self, li):
        enter_url = li.xpath("div[@class='name']/a/@href")
        enter_url = self.judge_null(enter_url)
        # enter_url = "http://www.anzhi.com" + enter_url
        return enter_url

    def get_version(self, inner_response):
        pat_version = '<span class="field">版本：</span>(.*?)</li>'
        version_num = re.findall(pat_version, inner_response)
        return version_num

    def get_img_address(self, li):
        selector = etree.HTML(self.inner_response)
        img_address = selector.xpath('//div[@class="Mpic Mpic72"]/img/@src')
        img_address = self.judge_null(img_address)
        return img_address

    def get_app_intro(self, inner_response):
        selector = etree.HTML(self.inner_response)
        app_intro = selector.xpath('//div[@class="bd"]/div/text()')
        app_intro = "".join(app_intro)
        # app_intro = self.judge_null(app_intro)
        if isinstance(app_intro, str):
            app_intro = app_intro.strip()
        return app_intro

if __name__ == '__main__':
    anzhi_spider = ShouJiZhuShou2345Spider(keyword="国信证券")
    anzhi_spider.parse()

