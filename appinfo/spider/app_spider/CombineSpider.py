from spider.app_spider.AnZhiSpider import AnZhiSpider
from spider.app_spider.ShouJiZhuShou2345Spider import ShouJiZhuShou2345Spider
from spider.app_spider.YingYongHuiSpider import YingYongHuiSpider
from spider.app_spider.YingYongBaoSpider import YingYongBaoSpider
from spider.app_spider.Zhushou360Spider import Zhushou360Spider
from spider.app_spider.BaiduZhuShouSpider import BaiduZhuShouSpider
from spider.app_spider.XiaoMiAppStoreSpider import XiaoMiAppStoreSpider
from spider.app_spider.PPZhuShouSpider import PPZhuShouSpider
from spider.app_spider.JinLiSpider import JinLiSpider
from spider.app_spider.SouGouSpider import SouGouSpider
from spider.app_spider.HuLiSpider import HuLiSpider
from spider.app_spider.LeShangDianSpider import LeShangDianSpider
from spider.app_spider.LiQvSpider import LiQvSpider
from spider.app_spider.AnBeiSpider import AnBeiSpider
from spider.app_spider.WoJi5577Spider import WoJi5577Spider
from spider.app_spider.FeiXiangSpider import FeiXiangSpider
from spider.app_spider.XiaZaiZhanPC6Spider import XiaZaiZhanPC6Spider
from spider.app_spider.ITMaoPuSpider import ITMaoPuSpider
from spider.app_spider.XinYuanSpider import XinYuanSpider
from spider.app_spider.XiXiRuanJianYuan import XiXiSpider
from spider.app_spider.YouQingSpider import YouQingSpider
from spider.app_spider.LvSeZiYuanWangSpider import LvSeZiYuanWangSpider
from spider.app_spider.LvSeXianFengSpider import LvSeXianFengSpider
from spider.app_spider.AnZhuo2265Spider import AnZhuo2265Spider
from spider.app_spider.BiKeEr import BiKeErSpider
from spider.app_spider.HuaJunRuanJianYuan import HuaJun
from spider.app_spider.XiTongZhiJia import XiTongZhiJIaSpider
from spider.app_spider.DangYiWang import DangYiWangSpider
from spider.app_spider.TaiPingYang import TaiPingYangSpider

class CombineSpider():
    @staticmethod
    def crawl(keyword):
        obj_list = [AnZhiSpider, ShouJiZhuShou2345Spider, YingYongHuiSpider, YingYongBaoSpider,
            Zhushou360Spider, BaiduZhuShouSpider, XiaoMiAppStoreSpider, PPZhuShouSpider, 
            JinLiSpider, SouGouSpider, HuLiSpider, LeShangDianSpider, LiQvSpider,
            AnBeiSpider, WoJi5577Spider, FeiXiangSpider, XiaZaiZhanPC6Spider, ITMaoPuSpider, 
            XinYuanSpider, XiXiSpider, YouQingSpider, LvSeZiYuanWangSpider, LvSeXianFengSpider,
            AnZhuo2265Spider, BiKeErSpider, HuaJun, XiTongZhiJIaSpider, DangYiWangSpider,TaiPingYangSpider
        ]
        for _cls in obj_list:
            spider = _cls(keyword)
            spider.parse()
            

# CombineSpider.crawl("国信证券开户")

# db = pymysql.connect("192.168.50.60", user="root", passwd="shuziguanxing123456", db="app_info")
# cursor = db.cursor()
# sql = """insert into spider_app(appStore, appName, version, updateTime, author,
#               downloadUrl, icon, introduction, inList, platform, insertTime) values(
#               'huawei', 'vpn', '1.3.4', '2020/7/7', 'tencent', 'http:sdfkljsdfkl', 'img',
#               'haohao', 'yeah', 'android', '2938/2/1')"""

# cursor.execute(sql)
# db.commit()

