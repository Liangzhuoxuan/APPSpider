from spider.app_spider.request_compoent import RqCompoent
from spider.app_spider.ParseCompoent import ParseComponent
from spider.app_spider.ParseComponentAjax import ParseComponentAjax
from lxml import etree
from urllib.parse import quote
import json
import re
import time


class PPZhuShouSpider(ParseComponentAjax):
    def __init__(self, keyword):
        super(PPZhuShouSpider, self).__init__("", keyword)
        # self.quote_keyword = "%7C" + quote(keyword)
        self.url = "https://server-m.pp.cn/StoreSearchController/search?ch=search_bz&ch_src=pp_upgrade_wap&uc_param_str=frvecpeimemintnidnut"
        self.n_page = 2
        self.name = "PP助手"

    def get_app_list_elements(self, url) -> list:
        add_headers = {"referer": "https://m.pp.cn/search.html"}
        self.add_headers = add_headers
        response = RqCompoent.post(url, data={"q": self.keyword, "page": "1"}, **add_headers)
        big_dict = json.loads(response)
        items = big_dict.get("data").get("content")
        return items

    def get_page_n_url(self, n=1):
        if n == 1:
            return self.url
        page_n_url = self.url.replace("reqPageNum=1", "reqPageNum={}".format(n))
        return page_n_url

    def get_app_name(self, item):
        app_name = item.get("name")
        return app_name

    def get_update_time(self, inner_response, item):
        # print(inner_response)
        # print(update_time)
        json_data = json.loads(inner_response)
        date = json_data.get("data").get("app").get("updateTime")
        timeArray = time.localtime(int(date // 1000))
        date = time.strftime("%Y-%m-%d", timeArray)
        return date

    def get_author(self, inner_response, item):
        """获取发行商"""
        # author_pat = 'detail-item-con">(.*?)</span>'
        # author = re.findall(author_pat, inner_response)
        # author = item.get("appDetail").get("authorName")
        json_data = json.loads(inner_response)
        author = json_data.get("data").get("app").get("seller")
        return author

    def get_download_url(self, inner_response, item):
        """获取下载地址"""
        # app_id_pat = 'opendown\((.*?)\);" title="下载到电脑"'
        # app_id = re.findall(app_id_pat, inner_response)

        download_url = item.get("downloadUrl")
        return download_url

    def get_enter_url(self, item):
        appid = item.get("id")
        enter_url = "https://server-m.pp.cn/StoreDetailController/detail?appId={}&ch_src=pp_upgrade_wap&ch=detail_bz&flags=6144&ppz=1&uc_param_str=frvecpeimemintnidnut".format(
            appid)
        # print("enter_url", enter_url)
        return enter_url

    def get_version(self, inner_response, item):
        """获取版本号"""
        # version = item.get("appVersionName")
        json_data = json.loads(inner_response)
        # version_pat = '版本(.*?)更新时间</span>'
        # version = re.findall(version_pat, inner_response, re.S)
        version = json_data.get("data").get("app").get("versionName")
        return version

    def get_img_address(self, item):
        # selector = etree.HTML(self.inner_response)
        # img_address = selector.xpath('//div[@class="detail-header"]/a/img/@src')
        # img_address = self.judge_null(img_address)
        json_data = json.loads(self.inner_response)
        img_address = json_data.get("data").get("app").get("iconUrl")
        return img_address

    def get_app_intro(self, inner_response):
        # selector = etree.HTML(inner_response)
        # app_intro = selector.xpath('//div[@class="detail-box"]/div[@id="introCont"]/text()')
        # app_intro = self.judge_null(app_intro)
        # if isinstance(app_intro, str):
        #     app_intro = app_intro.strip()
        json_data = json.loads(self.inner_response)
        app_intro = json_data.get("data").get("app").get("appDesc")
        return app_intro


if __name__ == '__main__':
    huawei_spider = PPZhuShouSpider(keyword="金太阳")
    huawei_spider.parse()
