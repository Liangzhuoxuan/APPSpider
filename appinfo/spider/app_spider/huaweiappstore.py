# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import requests
# import time

# keyword = "支付"

# driver = webdriver.Chrome()
# driver.get("https://appgallery1.huawei.com/#/search/%E6%94%AF%E4%BB%98")
# driver.maximize_window()
# driver.implicitly_wait(6)

# print(driver.page_source)

# apps = driver.find_elements_by_xpath('//div[@class="tem tem-l tem-big"]/div[@class="intro"]/div[1]/p[1]')
# l = len(apps)

# # for i in range(1, l+1):
# #     app = driver.find_element_by_xpath('//div[@class="tem tem-l tem-big"][{}]/img'.format(i))
# #     driver.implicitly_wait(3)
# #     app.click()
# #     driver.back()
# #     driver.implicitly_wait(3)
# for i in range(1, l+1):
#     app = driver.find_element_by_xpath('//div[@class="tem tem-l tem-big"][{}]/div[@class="intro"]/div[1]/p[1]'.format(i))
#     # app.click()
#     driver.execute_script("arguments[0].click();", app)
#     time.sleep(1.5)
#     driver.implicitly_wait(5)
#     driver.back()
#     time.sleep(1.5)
#     driver.implicitly_wait(5)

# time.sleep(2)
# driver.quit()

from request_compoent import RqCompoent
from ParseCompoent import ParseComponent
from ParseComponentAjax import ParseComponentAjax
from lxml import etree
from urllib.parse import quote
import json
import re
import time
import demjson



class HuaWeiAppStoreSpider(ParseComponentAjax):
    def __init__(self, keyword):
        super(HuaWeiAppStoreSpider, self).__init__("", keyword)
        self.url = "https://appgallery.cloud.huawei.com/uowap/index?method=internal.getTabDetail&maxResults=25&reqPageNum=1&serviceType=13&uri=searchApp%7C{}&locale=zh_CN".format(quote(keyword))
        self.n_page = 2
        self.name = "华为应用市场"

    def get_app_list_elements(self, url) -> list:
        response = RqCompoent.get(url)
        if not response:
            return [None, None, None, None]
        # big_dict = json.loads(response)
        big_dict = demjson.decode(response)
        items = big_dict.get("layoutData").get("dataList")
        return items

    def get_page_n_url(self, n):
        if n == 1:
            return self.url
        page_n_url = self.url.replace("&p=1", "&p={}".format(n))
        return page_n_url

    def get_app_name(self, item):
        if not item:
            return None
        app_name = item[1]
        # app_name = self.judge_null(app_name)
        # app_name = ''.join(re.findall("[\u4E00-\u9FFF]+", app_name))
        return app_name

    def get_update_time(self, inner_response, item):
        # print(inner_response)
        # pat_update_time = '<label>更新时间：</label>(.*?)</td>'
        # update_time = re.findall(pat_update_time, inner_response)
        # selector = etree.HTML(inner_response)
        # update_time = selector.xpath("//div[@class='det-main-container']/div[@class='det-othinfo-container J_Mod']/div[@class='det-othinfo-data']/@data-apkPublishTime")
        # update_time = item.get("appDetail").get("authorName")
        # update_time = self.judge_null(update_time).strip()
        if not item:
            return None
        return item[3]

    def get_author(self, inner_response, item):
        """获取发行商"""
        author_pat = '软件厂商:</span><b>(.*?)<'
        author = re.findall(author_pat, inner_response)
        # author = item.get("appDetail").get("authorName")
        author = self.judge_null(author).strip()
        return author

    def get_download_url(self, inner_response, li):
        """获取下载地址"""
        d_url_pat = 'href="http:(.*?)\.apk"'
        d_url = re.findall(d_url_pat, inner_response)
        download_url = self.judge_null(d_url)
        return download_url

    def get_enter_url(self, item):
        if not item:
            return None
        return item[0]

    def get_version(self, inner_response, item):
        """获取版本号"""
        # version = re.findall("<label>版本：</label>(.*?)</td>", inner_response)
        # version = self.judge_null(version).strip()
        if not item:
            return None
        return item[2]

    def get_img_address(self, item):
        # img_address = item[4]
        selector = etree.HTML(self.inner_response)
        img_address = selector.xpath('//ul[@class="info"]/li[1]/i/a/img/@src')
        img_address = self.judge_null(img_address)
        return img_address

    def get_app_intro(self, inner_response):
        selector = etree.HTML(inner_response)
        app_intro = selector.xpath('string(//div[@id="content"]//p)')
        app_intro = self.judge_null(app_intro)
        if isinstance(app_intro, str):
            app_intro = app_intro.strip()
        return app_intro

if __name__ == '__main__':
    itmaopu_spider = HuaWeiAppStoreSpider(keyword="支付")
    itmaopu_spider.parse()

