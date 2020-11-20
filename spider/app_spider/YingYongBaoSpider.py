from spider.app_spider.request_compoent import RqCompoent
from spider.app_spider.ParseCompoent import ParseComponent
from spider.app_spider.ParseComponentAjax import ParseComponentAjax
from lxml import etree
from urllib.parse import quote
import json
import re
import time


class YingYongBaoSpider(ParseComponentAjax):
    def __init__(self, keyword):
        super(YingYongBaoSpider, self).__init__("https://sj.qq.com/myapp/searchAjax.htm?kw=&pns=&sid=0", keyword)
        self.url = "https://sj.qq.com/myapp/searchAjax.htm?kw={}&pns=&sid=0".format(quote(keyword))
        self.n_page = 2
        self.name = "应用宝"

    def get_app_list_elements(self, url) -> list:
        response = RqCompoent.get(url)
        big_dict = json.loads(response)
        items = big_dict.get("obj").get("items")
        return items

    def get_page_n_url(self, n=2):
        if n == 1:
            return self.url
        page_letters = ['', 'MTA=', 'MjA=', 'MzA=']
        page_n_url = "https://sj.qq.com/myapp/searchAjax.htm?kw={}&pns={}&sid=0".format(self.quote_keyword, page_letters[n-1])
        return page_n_url

    def get_app_name(self, item):
        app_name = item.get("appDetail").get("appName")
        return app_name

    def get_update_time(self, inner_response, item):
        # print(inner_response)
        pat_update_time = 'id="J_ApkPublishTime" data-apkPublishTime="(.*?)"></div>'
        update_time = re.findall(pat_update_time, inner_response)
        # selector = etree.HTML(inner_response)
        # update_time = selector.xpath("//div[@class='det-main-container']/div[@class='det-othinfo-container J_Mod']/div[@class='det-othinfo-data']/@data-apkPublishTime")
        # update_time = item.get("appDetail").get("authorName")
        update_time = self.judge_null(update_time)

        # print(update_time)
        timeArray = time.localtime(int(update_time))
        date = time.strftime("%Y-%m-%d", timeArray)
        date = date.split('-')
        date = date[0] + '年' + date[1] + '月' + date[2] + '日'
        return date

    def get_author(self, inner_response, item):
        """获取发行商"""
        # author_pat = '作者：(.*?)</li>'
        # author = re.findall(author_pat, inner_response)
        author = item.get("appDetail").get("authorName")
        return author

    def get_download_url(self, inner_response, item):
        """获取下载地址"""
        # app_id_pat = 'opendown\((.*?)\);" title="下载到电脑"'
        # app_id = re.findall(app_id_pat, inner_response)
        
        download_url = item.get("appDetail").get("apkUrl")
        return download_url

    def get_enter_url(self, item):
        enter_url = item.get("pkgName")
        enter_url = "https://sj.qq.com/myapp/detail.htm?apkName=" + enter_url
        return enter_url

    def get_version(self, inner_response, item):
        """获取版本号"""
        version = item.get("appDetail").get("versionName")
        return version

    def get_img_address(self, item):
        # img_address = item[4]
        selector = etree.HTML(self.inner_response)
        img_address = selector.xpath('//div[@class="det-icon"]/img/@src')
        img_address = self.judge_null(img_address)
        return img_address

    def get_app_intro(self, inner_response):
        selector = etree.HTML(inner_response)
        app_intro = selector.xpath('string(//div[@class="det-app-data-info"])')
        app_intro = self.judge_null(app_intro)
        if isinstance(app_intro, str):
            app_intro = app_intro.strip()
        return app_intro


if __name__ == '__main__':
    yingyongbao_spider = YingYongBaoSpider(keyword="支付")
    yingyongbao_spider.parse()
