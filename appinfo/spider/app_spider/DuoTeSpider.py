from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from spider.app_spider.request_compoent import RqCompoent
from urllib.parse import quote
import re
import time


def judge_null(field):
    if field:
        return field[0].strip()
    else:
        return None


class DuoTeSpider():
    @staticmethod
    def run(keyword):
        chrome_opt = Options()
        chrome_opt.add_argument("--headless")
        chrome_opt.add_argument("--disable-gpu")
        chrome_opt.add_argument("--no-sandbox")
        driver = webdriver.Chrome(chrome_options=chrome_opt)
        # driver = webdriver.Chrome()
        driver.get("http://s.duote.com:8081/searchandroid/androidindex/?keywords=" + quote(keyword, encoding="GBK"))
        driver.maximize_window()
        driver.implicitly_wait(6)

        start_handle = driver.current_window_handle

        # //div[@class='listWrapper'][{}]/div[@class='list']/dl[@class='result']/dt/a
        elems = driver.find_elements_by_xpath("//div[@class='listWrapper']/div[@class='list']/dl[@class='result']/dt/a")
        print(len(elems))
        for i in range(1, len(elems) + 1):
            xpath = f"//div[@class='listWrapper'][{i}]/div[@class='list']/dl[@class='result']/dt/a"
            ele = driver.find_element_by_xpath(xpath)
            ele.click()
            driver.implicitly_wait(6)
            time.sleep(1)
            handles = driver.window_handles

            for handle in handles:
                if handle != start_handle:
                    driver.switch_to.window(handle)
                    page_source = driver.page_source
                    app_store = "多特下载"
                    app_name = None
                    version = None
                    updateTime = None
                    author = None
                    download_url = None
                    icon = None
                    introduction = None
                    enter_url = None
                    if "很抱歉，页面没有找到" not in page_source:
                        app_name = re.findall("<h1>(.*?)</h1>", page_source)
                        version = re.findall("版本:</span>(.*?)<", page_source, re.S)
                        updateTime = re.findall("更新:</span>(.*?)<", page_source, re.S)
                        # 没有开发商信息
                        download_url = driver.find_element_by_xpath("//div[@class='versionWrap']/a").get_attribute(
                            "href")
                        icon = driver.find_element_by_xpath("//div[@class='softImg']/img").get_attribute("src")
                        introduction = driver.find_element_by_id("soft-intr").text
                        app_name = judge_null(app_name)
                        version = judge_null(version)
                        updateTime = judge_null(updateTime)

                        print(app_name, version, updateTime, download_url, icon, introduction[:10])
                    enter_url = driver.current_url
                    driver.close()
                    driver.switch_to.window(handles[0])

        driver.quit()


if __name__ == '__main__':
    DuoTeSpider.run("金太阳")
