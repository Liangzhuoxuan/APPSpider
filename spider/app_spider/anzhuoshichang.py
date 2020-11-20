import urllib
from lxml import etree
import re
from request_compoent import RqCompoent


def parse(response, url, keyword):
    selector = etree.HTML(response)
    lis = selector.xpath("//div[@class='app_list border_three']/ul//li")

    flag = 1
    for li in lis:
        temp_element = li.xpath("div[@class='app_info']/span[@class='app_name']/a")[0]
        app_name = temp_element.xpath("text()")[0]  # app_name
        app_url = temp_element.xpath("@href")[0]
        # print(app_name)
        if app_name == keyword:
            base_url = "http://www.anzhi.com"
            parse_second(base_url + app_url)
            flag = 0
            break

    def parse_one_page(lis):
        '''解析一页'''
        for li in lis:
            temp_element = li.xpath("div[@class='app_info']/span[@class='app_name']/a")[0]
            app_name = temp_element.xpath("text()")[0]  # app_name
            app_url = temp_element.xpath("@href")[0]
            base_url = "http://www.anzhi.com"
            parse_second(base_url + app_url)
            # 验证
            # print(app_name)

    if flag:
        parse_one_page(lis)
        # 获取前两页的信息
        page_two_response = RqCompoent.get(url + "&page=2")
        _selector = etree.HTML(page_two_response)
        _lis = _selector.xpath("//div[@class='app_list border_three']/ul//li")
        parse_one_page(_lis)


def parse_second(_url):
    response = RqCompoent.get(_url)
    # 版本号
    pat_version = '<span class="app_detail_version">\((.*?)\)</span>'
    version_num = re.findall(pat_version, response)
    if version_num:
        version_num = version_num[0]
    # 更新时间
    pat_update_time = '时间：(.*?)</li>'
    update_time = re.findall(pat_update_time, response)
    if update_time:
        update_time = update_time[0]
    # 开发商
    author_pat = '作者：(.*?)</li>'
    author = re.findall(author_pat, response)
    if author:
        author = author[0]
    app_id_pat = 'opendown\((.*?)\);" title="下载到电脑"'
    app_id = re.findall(app_id_pat, response)[0]
    download_link = "http://www.anzhi.com/dl_app.php?s=" + app_id + "&n=5"

    print(version_num, update_time, author, download_link)
    # app名称，平台，版本号，应用市场，是否在客户提供清单中，更新日期，下载链接，开发商


def _run(keyword):
    # keyword = "国信证券开户"
    # %E5%B9%BF%E5%8F%91%E8%AF%81%E5%88%B8%E5%BC%80%E6%88%B7
    url = "http://www.anzhi.com/search.php?keyword="
    encoded_keyword = urllib.parse.quote(keyword)
    url = url + encoded_keyword
    response = RqCompoent.get(url)
    parse(response, url, keyword)


if __name__ == '__main__':
    _run("支付")
