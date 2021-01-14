from lxml import etree
import urllib
import re
from spider.app_spider.request_compoent import RqCompoent
from time import sleep
import pymysql
import time

class ParseComponent(object):
    def __init__(self, url, keyword):
        self.keyword = keyword
        # 对 url 里面的中文字符进行编码
        self.quote_keyword = urllib.parse.quote(keyword)
        # self.url = url + self.quote_keyword
        self.match_keyword = False
        self.delay_time = 0.05
        self.add_headers = {}
        self.n_page = 1
        self.name = "xx应用市场"    
        self.db = pymysql.connect("192.168.50.60", user="root", passwd="shuziguanxing123456", db="app_info")
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
        for i in range(1, self.n_page+1):
            page_n_url = self.get_page_n_url(i)
            try:
                lis = self.get_app_list_elements(page_n_url)
            except:
                lis = None
            if not lis:
                continue
            if lis == "error":
                continue
            # 比对关键字，如果全部匹配，则只取这一个app的信息
            # 如果匹配不上，则把前 n 页的app信息爬下来
            if i == 1:
                self.loop_request(lis, first_page=True)
            else:
                self.loop_request(lis, first_page=False)

    def parse_app_info_page(self, inner_response):
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
            update_time = self.get_update_time(inner_response)
        except:
            pass
        try:
            author = self.get_author(inner_response)
        except:
            pass
        try:
            download_url = self.get_download_url(inner_response)
        except:
            pass
        try:
            version = self.get_version(inner_response)
        except:
            pass
        # # 判断是否为空列表
        update_time = self.judge_null(update_time)
        author = self.judge_null(author)
        version = self.judge_null(version)
        download_url = self.judge_null(download_url)
        if update_time:
            update_time = re.sub("[年月日]", '/', update_time)
        return [version, update_time, author, download_url]

    def get_app_list_elements(self, url) -> list:
        """
        获取搜索结果列表对应的元素
        :return: 搜索结果元素列表
        """
        response = RqCompoent.get(url)
        if not response:
            return "error"
        self.outer_response = response
        selector = etree.HTML(response)
        lis = selector.xpath()
        return lis

    def get_enter_url(self, li, *args, **kwargs):
        """获取详情页的 url"""
        enter_url = li.xpath()
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

    def loop_request(self, lis, first_page=True, **kwargs):
        """循环请求"""

        if not lis:
            return 
        # for li in lis:
        #     app_name = self.get_app_name(li)  # 先获取一下app名字，对比关键字
        #     app_name = self.judge_null(app_name)
        #     app_name = self.field_strip(app_name)
        #     if first_page:
        #         if self.keyword == app_name:
        #             enter_url = self.get_enter_url(li)  # 获取详情页url
        #             inner_response = RqCompoent.get(enter_url)
        #             fields = self.parse_app_info_page(inner_response)
        #             to_sink = [app_name, *fields]
        #             print(*to_sink)
        #             self.match_keyword = True
        #             break
        #     else:
        #         enter_url = self.get_enter_url(li)  # 获取详情页url
        #         inner_response = RqCompoent.get(enter_url)
        #         fields = self.parse_app_info_page(inner_response)
        #         to_sink = [app_name, *fields]
        #         print(*to_sink)
        #     sleep(self.delay_time)

        # # 爬第一页的所有app信息
        # if not self.match_keyword:
        #     for li in lis:
        #         app_name = self.get_app_name(li)  # 先获取一下app名字，对比关键字
        #         app_name = self.judge_null(app_name)
        #         app_name = self.field_strip(app_name)
        #         enter_url = self.get_enter_url(li)  # 获取详情页url
        #         inner_response = RqCompoent.get(enter_url)
        #         fields = self.parse_app_info_page(inner_response)
        #         to_sink = [app_name, *fields]
        #         print(*to_sink)
        #         sleep(self.delay_time)
        for li in lis:
            enter_url = None
            try:
                enter_url = self.get_enter_url(li)  # 获取详情页url
            except:
                pass
            inner_response = RqCompoent.get(enter_url, **self.add_headers)
            if inner_response:
                self.inner_response = inner_response
                self.li = li

                app_name = None
                img_address = None
                app_intro = None
                try:
                    app_name = self.get_app_name(li)  # 先获取一下app名字，对比关键字
                except:
                    pass
                app_name = self.judge_null(app_name)
                app_name = self.field_strip(app_name)
                try:
                    img_address = self.get_img_address(li)
                except:
                    pass
                try:
                    app_intro = self.get_app_intro(inner_response)
                except:
                    pass
                fields = self.parse_app_info_page(inner_response)
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

    def get_app_name(self, li, *args, **kwargs):
        """获取 app 名称
        如果不是直接用li，用当页的response，从 kwargs 里面传参
        """
        app_name = li.xpath()
        return app_name

    def get_version(self, inner_response):
        """获取版本号"""
        version = None
        return version

    def get_update_time(self, inner_response):
        """获取更新时间"""
        update_time = None
        return update_time

    def get_author(self, inner_response):
        """获取发行商"""
        author = None
        return author

    def get_download_url(self, inner_response):
        """获取下载地址"""
        download_url = None
        return download_url

    def get_img_address(self, li):
        img_address = None
        return img_address

    def get_app_intro(self, inner_response, *args):
        app_intro = None
        return app_intro

    def parse(self):
        self.parse_app_list_page()
