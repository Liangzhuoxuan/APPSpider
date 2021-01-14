from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from spider.app_spider.request_compoent import RqCompoent
from lxml import etree
import re
import time


def judge_null(field):
    if isinstance(field, str):
        return field
    if field:
        return field[0]
    else:
        return None


class WanDouJia():
    @staticmethod
    def run():
        keyword = "支付"
        driver = webdriver.Chrome()
        driver.get("https://www.wandoujia.com/")
        driver.maximize_window()
        driver.implicitly_wait(6)

        search_input = driver.find_element_by_xpath('//input[@class="key-ipt"]')
        search_input.clear()
        search_input.send_keys(keyword)
        search_input.send_keys(Keys.ENTER)
        driver.implicitly_wait(6)

        # 切换到指定元素的位置
        move_to = driver.find_element_by_partial_link_text("查看更多")
        ActionChains(driver).move_to_element(move_to).perform()
        move_to.click()
        time.sleep(2)
        driver.implicitly_wait(2)

        page_source = driver.page_source
        selector = etree.HTML(page_source)

        enter_urls = selector.xpath('//h2[@class="app-title-h2"]/a/@href')
        print(enter_urls)
        # time.sleep(3)
        driver.quit()
        for enter_url in enter_urls:
            response = RqCompoent.get(enter_url)
            selector = etree.HTML(response)
            app_name = judge_null(selector.xpath('//span[@class="title"]/text()'))
            download_url = judge_null(selector.xpath('//div[@class="download-wp"]/a[2]/@href'))
            update_time = judge_null(selector.xpath('//span[@class="update-time"]/text()'))
            if update_time:
                update_time = update_time.split(":")[1].strip()
            version = judge_null(re.findall("版本</dt><dd>(.*?)<", response, re.S))
            if version:
                version = version.split(";")[1].strip()
            author = judge_null(re.findall("开发者</dt><dd><.*?>([\u4E00-\u9FA5]+)<", response, re.S))
            img = judge_null(selector.xpath('//div[@class="app-icon"]/img/@src'))
            intro = judge_null(selector.xpath('string(//div[@class="desc-info"]/div/div)'))
            print(app_name, download_url, update_time, version, author, img, intro)

            # 清洗一下，换一下顺序即可
            row = ["豌豆荚", app_name, version, update_time, author, download_url, img, intro]


if __name__ == '__main__':
    run()
