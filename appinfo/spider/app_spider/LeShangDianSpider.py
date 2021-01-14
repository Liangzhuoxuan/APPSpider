from spider.app_spider.request_compoent import RqCompoent
from spider.app_spider.ParseCompoent import ParseComponent
from spider.app_spider.ParseComponentAjax import ParseComponentAjax
from lxml import etree
from urllib.parse import quote
import json
import re
import time


# 这个兄弟中间会加入很多热门数据，暂时只爬2页吧，第三页开始都是热门数据
class LeShangDianSpider(ParseComponentAjax):
    def __init__(self, keyword):
        super(LeShangDianSpider, self).__init__("", keyword)
        self.url = "https://www.lenovomm.com/api/search?kw={}&si=0&cnt=40".format(quote(keyword))
        self.n_page = 1
        self.name = "乐商店"

    def get_app_list_elements(self, url) -> list:
        response = RqCompoent.get(url)
        # response = re.findall("jQuery191018405249964393477_1594619120728\((.*?)\);", response, re.S)[0]
        big_dict = json.loads(response)
        items = big_dict.get("result").get("docs")
        return items

    def get_page_n_url(self, n):
        if n == 1:
            return self.url
        page_n_url = self.url.replace("&page=1", "&page={}".format(n))
        return page_n_url

    def get_app_name(self, item):
        app_name = item.get("appname")
        # app_name = self.judge_null(app_name)
        # app_name = ''.join(re.findall("[\u4E00-\u9FFF]+", app_name))
        return app_name

    def get_update_time(self, inner_response, item):
        # print(inner_response)
        # pat_update_time = '更新时间：(.*?)</div>'
        # update_time = re.findall(pat_update_time, inner_response)
        # selector = etree.HTML(inner_response)
        # update_time = selector.xpath("//div[@class='det-main-container']/div[@class='det-othinfo-container J_Mod']/div[@class='det-othinfo-data']/@data-apkPublishTime")
        # update_time = item.get("appDetail").get("authorName")
        # update_time = self.judge_null(update_time).strip()
        update_time = item.get("publishdate")
        return update_time

    def get_author(self, inner_response, item):
        """获取发行商"""
        # author_pat = '开发商：(.*?)</div>'
        # author = re.findall(author_pat, inner_response)
        # author = item.get("appDetail").get("authorName")
        # author = self.judge_null(author).strip()
        return None

    def get_download_url(self, inner_response, item):
        """获取下载地址"""
        d_pat = '<a class="download" href="(.*?)">下载</a>'
        d_url = re.findall(d_pat, inner_response)
        d_url = self.judge_null(d_url)
        # download_url = li.xpath("a/@apkurl")
        # download_url = item.get("downloadurl")
        return d_url

    def get_enter_url(self, item):
        # {"code":"AMS-308","timestamp":1594622049693,"detail":"clientId为空无法获取ClientInfo信息！clientid=null"}
        app_id = item.get("appversioncode")
        app_pack = item.get("apppack")
        # enter_url = "http://m.anzhuoapk.com/mobile/soft/detail/" + app_id
        enter_url = "https://www.lenovomm.com/appdetail/{}/{}".format(app_pack, app_id)
        return enter_url

    def get_version(self, inner_response, item):
        """获取版本号"""
        # version = re.findall("<label>版本：</label>(.*?)</td>", inner_response)
        # version = self.judge_null(version).strip()
        version = item.get("appversion")
        return version

    def get_img_address(self, item):
        # img_address = item[4]
        selector = etree.HTML(self.inner_response)
        img_address = selector.xpath('//div[@class="info_con"]/img/@src')
        img_address = self.judge_null(img_address)
        return img_address

    def get_app_intro(self, inner_response):
        # selector = etree.HTML(inner_response)
        # app_intro = selector.xpath('//div[@class="description-wrapper"]/div[2]/text()')
        # app_intro = self.judge_null(app_intro)
        # if isinstance(app_intro, str):
        #     app_intro = app_intro.strip()
        return []


if __name__ == '__main__':
    le_spider = LeShangDianSpider(keyword="支付")
    le_spider.parse()
