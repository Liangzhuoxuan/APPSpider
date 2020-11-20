import requests
import time
from hashlib import md5


secret = "6508ddd843e78d9350b787ae81c8420e"
orderId = "DT20200410155216L1evf4mh"
timestamp = str(int(time.time()))

txt = "orderno={},secret={},timestamp={}".format(orderId, secret, timestamp)
sign = md5(txt.encode()).hexdigest().upper()

headers = {
    "Proxy-Authorization": "sign={}&orderno={}&timestamp={}&change=true".format(sign, orderId, timestamp),
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    }

proxies = {"http": "http://" + "dynamic.xiongmaodaili.com:8088",
            "https": "https://" + "dynamic.xiongmaodaili.com:8088"}

response = requests.get("http://s.itmop.com/search/pc/%E6%94%AF%E4%BB%98_all_hits.html", headers=headers, proxies=proxies)
print(response.status_code)
print(response.content.decode())

