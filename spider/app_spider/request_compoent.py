import requests
import chardet
from hashlib import md5
import time
import random


def get_random_ua(app=False) -> list:
    andriod_ua = [
        "Mozilla/5.0 (Linux; Android 9; PAFM00 Build/PKQ1.190319.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.18 lite baiduboxapp/4.12.0.11 (Baidu; P1 9)",
        "Mozilla/5.0 (Linux; Android 6.0; BLN-AL10 Build/HONORBLN-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/11.16 SP-engine/2.12.0 baiduboxapp/11.16.2.10 (Baidu; P1 6.0)",
        "Mozilla/5.0 (Linux; Android 8.1.0; OPPO R11 Build/OPM1.171019.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 8.1.0)",
        "Mozilla/5.0 (Linux; Android 9; MI CC 9 Build/PKQ1.181121.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045114 Mobile Safari/537.36 V1_AND_SQ_8.2.7_1334_YYB_D QQ/8.2.7.4410 NetType/4G WebP/0.3.0 Pixel/1080 StatusBarHeight/75 SimpleUISwitch/1",
        "Mozilla/5.0 (Linux; Android 9; vivo X21A Build/PKQ1.180819.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045008 Mobile Safari/537.36 V1_AND_SQ_8.2.6_1320_YYB_D QQ/8.2.6.4370 NetType/4G WebP/0.3.0 Pixel/1080 StatusBarHeight/84 SimpleUISwitch/0",
    ]

    pc_ua = [
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    ]

    if app:
        return random.choice(andriod_ua)

    return random.choice(pc_ua)


def return_headers_and_proxies(app=False):
    """随机选择当前此次请求是否使用代理"""
    if not app:
        headers = {
            "User-Agent": get_random_ua(app=False),
        }
    else:
        headers = {
            "User-Agent": get_random_ua(app=True),
        }

    proxies = None
    seed = [1, 2, 3, 4]  # 1/5 概率使用代理
    result = random.choice(seed)
    if not result:
        secret = "6508ddd843e78d9350b787ae81c8420e"
        orderId = "DT20200410155216L1evf4mh"
        timestamp = str(int(time.time()))
        txt = "orderno={},secret={},timestamp={}".format(orderId, secret, timestamp)
        sign = md5(txt.encode()).hexdigest().upper()
        headers = {**headers, **{
            "Proxy-Authorization": "sign={}&orderno={}&timestamp={}&change=true".format(sign, orderId, timestamp)}}
        proxies = {
            "http": "http://" + "dynamic.xiongmaodaili.com:8088",
            "https": "https://" + "dynamic.xiongmaodaili.com:8088"
        }

    return headers, proxies


class RqCompoent():

    @staticmethod
    def get(url, app=False, *args, **kwargs):
        # 请求代理 && 随机获取请求头
        headers, proxies = return_headers_and_proxies(app)
        # 扩展请求头
        headers = {**headers, **kwargs}
        # s = requests.session()
        # response = requests.get(url, headers=headers)
        if not url:
            return None
        if not proxies:
            response = requests.get(url, headers=headers)
        else:
            response = requests.get(url, headers=headers, proxies=proxies)

        if response.status_code == 200:
            try:
                response = response.content  # 得到字节
                charset = chardet.detect(response).get('encoding')  # 得到编码格式
                # print(charset)
                response = response.decode(charset, "ignore")  # 解码得到字符串
                return response
            except:
                return None
        else:
            print("请求失败")
            return None

    @staticmethod
    def post(url, data, app=False, *args, **kwargs):
        headers, proxies = return_headers_and_proxies(app)
        # 扩展请求头
        if not url:
            return None
        headers = {**headers, **kwargs}
        if not proxies:
            response = requests.post(url, headers=headers, data=data, timeout=6)
        else:
            response = requests.post(url, headers=headers, data=data, proxies=proxies, timeout=6)
        # response = requests.post(url, headers=headers, data=data, timeout=10)
        if response.status_code == 200:
            response = response.content
            charset = chardet.detect(response).get('encoding')  # 得到编码格式
            response = response.decode(charset, "ignore")  # 解码得到字符串
            return response
        else:
            print("请求失败")
