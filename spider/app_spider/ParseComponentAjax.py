from lxml import etree
import urllib
import re
from spider.app_spider.request_compoent import RqCompoent
from time import sleep
import json
import pymysql
import time


class ParseComponentAjax(object):
    def __init__(self, url, keyword):
        self.keyword = keyword
        # 对 url 里面的中文字符进行编码
        self.quote_keyword = urllib.parse.quote(keyword)
        # self.url = url + self.quote_keyword
        self.match_keyword = False
        self.delay_time = 0.1
        self.add_headers = {}
        self.n_page = 1
        self.name = "xx应用市场"
        self.db = pymysql.connect(
            "192.168.50.60", user="root", passwd="shuziguanxing123456", db="app_info")
        self.cursor = self.db.cursor()

    def combine_url_keyword(self):
        pass

    def get_page_n_url(self, n):
        """返回前 n 页的 url"""
        if n == 1:
            return self.url
        # 返回从第二页开始的 url
        page_n_url = self.url + "&page={}".format(n)
        return page_n_url

    def parse_app_list_page(self):
        """
        1.遍历匹配关键字
        2.匹配成功则只爬那一个
        3.匹配失败则把前 n 页的数据爬下来，默认值为 2
        :return:
        """
        for i in range(1, self.n_page + 1):
            page_n_url = self.get_page_n_url(i)
            try:
                lis = self.get_app_list_elements(page_n_url)
            except:
                lis = None
            if not lis:
                continue
            # 比对关键字，如果全部匹配，则只取这一个app的信息
            # 如果匹配不上，则把前 n 页的app信息爬下来
            if i == 1:
                self.loop_request(lis, first_page=True)
            else:
                self.loop_request(lis, first_page=False)

    def parse_app_info_page(self, inner_response, item):
        """
        四个字段
        1.App名称 这个在外层获取了
        2.更新时间
        3.发行商
        4.下载地址
        :return:
        """
        update_time = None
        author = None
        download_url = None
        version = None
        try:
            update_time = self.get_update_time(inner_response, item)
        except:
            pass
        try:
            author = self.get_author(inner_response, item)
        except:
            pass
        try:
            download_url = self.get_download_url(inner_response, item)
        except:
            pass
        try:
            version = self.get_version(inner_response, item)
        except:
            pass
        if update_time:
            update_time = re.sub("[年月日]", '/', update_time)
        # 判断是否为空列表
        # update_time = self.judge_null(update_time)
        # author = self.judge_null(author)
        # version = self.judge_null(version)
        # download_url = self.judge_null(download_url)
        return [version, update_time, author, download_url]

    def get_app_list_elements(self, url) -> list:
        """
        获取搜索结果列表对应的元素
        :return: 搜索结果元素列表
        """
        response = RqCompoent.get(url)
        big_dict = json.loads(response)
        print(big_dict)
        items = []
        # selector = etree.HTML(response)
        # lis = selector.xpath()

        # return lis
        return items

    def get_enter_url(self, item):
        """获取详情页的 url"""
        enter_url = item[""]
        return enter_url

    def judge_null(self, field):
        """判断是否为空列表"""
        if isinstance(field, str):
            return field

        if field:
            field = field[0]
            return field

        return None

    def field_strip(self, field):
        if isinstance(field, str):
            return field.strip()
        else:
            return field

    def temp_request(self, enter_url, method="get", data={}):
        if method == "get":
            inner_response = RqCompoent.get(enter_url, **self.add_headers)
        else:
            inner_response = RqCompoent.post(
                enter_url, data, **self.add_headers)

    def loop_request(self, items, first_page=True):
        """循环请求"""
        if not items:
            return
        # # 爬第一页的所有app信息
        # if not self.match_keyword:
        for item in items:
            try:
                enter_url = self.get_enter_url(item)  # 获取详情页url
            except:
                pass
            if not enter_url:
                continue
            app_name = None
            img_address = None
            app_intro = None
            try:
                inner_response = RqCompoent.get(enter_url, **self.add_headers)
            except:
                inner_response = None
            if inner_response:
                self.item = item
                self.inner_response = inner_response
                try:
                    app_name = self.get_app_name(item)  # 先获取一下app名字，对比关键字
                except:
                    pass
                # app_name = self.judge_null(app_name)
                app_name = self.field_strip(app_name)
                try:
                    img_address = self.get_img_address(item)
                except:
                    pass
                try:
                    app_intro = self.get_app_intro(inner_response)
                except:
                    pass
                fields = self.parse_app_info_page(inner_response, item)
                to_sink = [self.name, app_name, *fields, img_address, app_intro]
                res = []
                for i in to_sink:
                    if not i:
                        res.append(None)
                    else:
                        res.append(pymysql.escape_string(i))
                try:
                    print(*res[:-1], res[-1][:20])
                except:
                    pass
                sql = "insert into spider_app(appStore, appName, version, updateTime, author,downloadUrl,icon, introduction, inList, platform, insertTime, keyword, enter_url) values(%s, %s, %s, %s, %s, %s, %s, %s, '否', '安卓', %s, %s, %s)"
                res = [*res, pymysql.escape_string(time.strftime("%Y/%m/%d", time.localtime())), pymysql.escape_string(self.keyword), pymysql.escape_string(enter_url)]
                try:
                    self.cursor.execute(sql, res)
                except:
                    pass
                sleep(self.delay_time)
        self.db.commit()

    def fixed_enter_url(self, enter_url):
        """修正进入详情页的链接"""
        # enter_url = "主域名" + enter_url
        return enter_url

    def get_app_name(self, item):
        """获取 app 名称"""
        app_name = item[""]
        return app_name

    def get_version(self, inner_response, item):
        """获取版本号"""
        version = None
        return version

    def get_update_time(self, inner_response, item):
        """获取更新时间"""
        update_time = None
        return update_time

    def get_author(self, inner_response, item):
        """获取发行商"""
        author = None
        return author

    def get_download_url(self, inner_response, item):
        """获取下载地址"""
        download_url = None
        return download_url

    def get_img_address(self, item):
        img_address = None
        return img_address

    def get_app_intro(self, inner_response, *args):
        app_intro = None
        return app_intro

    def parse(self):
        self.parse_app_list_page()


if __name__ == '__main__':
    x = ParseComponentAjax(
        "https://wap1.hispace.hicloud.com/uowap/index?method=internal.getTabDetail&serviceType=20&reqPageNum=1&uri=searchApp%7C%E6%94%AF%E4%BB%98&maxResults=25&version=10.0.0&zone=&locale=zh_CN", "%7C%E6%94%AF%E4%BB%98")
