from spider.app_spider.request_compoent import RqCompoent
from spider.app_spider.ParseCompoent import ParseComponent
from spider.app_spider.ParseComponentAjax import ParseComponentAjax
from lxml import etree
from urllib.parse import quote
import json
import re
import time


class SouGouSpider(ParseComponentAjax):
    def __init__(self, keyword):
        super(SouGouSpider, self).__init__("http://zhushou.sogou.com/apps/search.html?key=&act=getapp", keyword)
        self.url = "http://zhushou.sogou.com/apps/search.html?key={}&act=getapp&page=1".format(quote(keyword))
        self.n_page = 1
        # self.delay_time = 2
        self.name = "搜狗应用市场"

    def get_app_list_elements(self, url) -> list:
        response = RqCompoent.get(url)
        if response:
            big_dict = json.loads(response)
            items = big_dict.get("data")
            return items

    def get_page_n_url(self, n):
        if n == 1:
            return self.url
        page_n_url = self.url.replace("&page=1", "&page={}".format(n))
        return page_n_url

    def get_app_name(self, item):
        app_name = item.get("name")
        # app_name = self.judge_null(app_name)
        app_name = ''.join(re.findall("[\u4E00-\u9FFF]+", app_name))
        return app_name

    def get_update_time(self, inner_response, item):
        # print(inner_response)
        pat_update_time = '<label>更新时间：</label>(.*?)</td>'
        update_time = re.findall(pat_update_time, inner_response)
        # selector = etree.HTML(inner_response)
        # update_time = selector.xpath("//div[@class='det-main-container']/div[@class='det-othinfo-container J_Mod']/div[@class='det-othinfo-data']/@data-apkPublishTime")
        # update_time = item.get("appDetail").get("authorName")
        update_time = self.judge_null(update_time).strip()
        return update_time

    def get_author(self, inner_response, item):
        """获取发行商"""
        author_pat = '<label>作者：</label>(.*?)</td>'
        author = re.findall(author_pat, inner_response)
        # author = item.get("appDetail").get("authorName")
        author = self.judge_null(author).strip()
        return author

    def get_download_url(self, inner_response, li):
        """获取下载地址"""
        # app_id_pat = 'opendown\((.*?)\);" title="下载到电脑"'
        # app_id = re.findall(app_id_pat, inner_response)
        # download_url = li.xpath("a/@apkurl")
        # if download_url:
        #     download_url = download_url[0]
        # download_url = "http://m.anzhuoapk.com" + download_url
        res = None
        try:
            res = RqCompoent.get("http://zhushou.sogou.com/apps/download.html?appid={}".format(self.app_id))
        except:
            pass
        if not res:
            return None
        j = json.loads(res)
        download_url = j.get("data").get("file_url")
        return download_url

    def get_enter_url(self, item):
        enter_url = item.get("url")
        app_id = enter_url.split("/")[-1].split(".")[0]
        self.app_id = app_id
        # if app_id:
        #     app_id = app_id[0]
        # else:
        #     app_id = ""
        # enter_url = "http://m.anzhuoapk.com/mobile/soft/detail/" + app_id
        return enter_url

    def get_version(self, inner_response, item):
        """获取版本号"""    
        version = re.findall("<label>版本：</label>(.*?)</td>", inner_response)
        version = self.judge_null(version).strip()
        return version

    def get_img_address(self, item):
        # img_address = item[4]
        selector = etree.HTML(self.inner_response)
        img_address = selector.xpath('//div[@class="overview"]/img[@class="icon"]/@src')
        img_address = self.judge_null(img_address)
        return img_address

    def get_app_intro(self, inner_response):
        selector = etree.HTML(inner_response)
        app_intro = selector.xpath('//div[@class="article"]/div[1]/div/text()')
        app_intro = self.judge_null(app_intro)
        if isinstance(app_intro, str):
            app_intro = app_intro.strip()
        return app_intro

if __name__ == '__main__':
    sougou_spider = SouGouSpider(keyword="支付")
    sougou_spider.parse()
