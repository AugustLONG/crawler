# -*- coding: utf-8 -*-

import logging
from xml.dom import minidom

import scrapy

from crawler.utils.xml import get_attrvalue, get_nodevalue, get_xmlnode

logger = logging.getLogger("NuomiSpider")
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

cities = "aba, akesu, alashan, ali, altay, anji, ankang, anqing, anqiu, anshan, anshun, anyang, aomen, artux, baicheng, baise, baisha, baishan, baiyin, baoding, baoji, baoshan, baoting, baotou, bayangolmongol, bayannaoer, bazhong, beihai, beijing, bengbu, benxi, bijie, binzhou, boertalamongol, bozhou, cangzhou, changchun, changde, changdu, changji, changjiang, changsha, changshu, changxing, changzhi, changzhou, chaohu, chaoyang, chaozhou, chengde, chengdu, chengmai, chenzhou, chifeng, chizhou, chongqing, chongzuo, chunan, chuxiong, chuzhou, cixi, dafeng, daidehongjingpo, dali, dalian, dandong, danzhou, daqing, datong, daxinganling, dazhou, dengfeng, deqing, deyang, dezhou, dingan, dingxi, diqing, dongfang, dongguan, dongyang, dongying, dunhua, eerduosi, emeishan, enshi, ezhou, fangchenggang, fenghuang, foshan, fuqing, fushun, fuxin, fuyang, fuyang1, fuzhou, fuzhou1, gannan, ganzhou, ganzizhou, gongyi, guangan, guangyuan, guangzhou, guigang, guilin, guiyang, guoluo, guyuan, haerbin, haian, haibei, haidong, haikou, haimen, hainantibetan, haining, haixi, hami, handan,hangzhou, hanzhong, hebi, hechi, hefei, hegang, heihe, hengshui, hengyang, hetian, heyuan, heze, hezhou, hohhot, honghe, huadian, huaian, huaibei, huaihua, huainan, huanggang, huangnan, huangshan, huangshi, huizhou, huludao, hulunbeier, huzhou, jiamusi, jian, jiande, jiangmen, jiangyin, jiaozuo, jiashan, jiaxing, jiayuguan, jieshou, jieyang, jilin, jinan, jinchang, jincheng, jindezhen, jingjiang, jingmen, jingzhou, jinhua, jining, jinjiang, jintan, jinzhong, jinzhou, jiujiang, jiuquan, jiuzhaigou, jixi, jiyuan, kaifeng, kashgar, kelamayi, kunming, kunshan, laibin, laiwu, langfang, lanxi, lanzhou, lasa, ledong, leqing, leshan, liangshan, lianyungang, liaocheng, liaoning, liaoyang, liaoyuan, lijiang, linan, lincang, linfen, lingao, lingshui, linhai, lintong, linxia, linxiaa, linyi, lishui, liuan, liupanshui, liuzhou, liyang, longkou, longnan, longsheng, longyan, loudi, luohe, luoyang, luzhou, lvliang, maanshan, manzhouli, maoming, meishan, meizhou, mianyang,mingguang, mudanjiang, nanchang, nanchong, nanjing, nanning, nanping, nantong, nanyang, naqu, neijiang, ningbo, ningde, ningguo, nujianglisuzu, nyingchi, panjin, panzhihua, pingdingshan, pinghu, pingliang, pingxiang, puer, putian, puyang, qiandongnanmiaodongautonomous, qiannan, qianxinan, qidong, qingdao, qingyang, qingyuan, qingzhou, qinhuangdao, qinzhou, qionghai, qiongzhong, qiqihar, qitaihe, qizhou, quanzhou, qufu, qujing, quzhou, rikaze, rizhao, rugao, ruian, sanhe, sanmenxia, sanming, sanya, shanghai, shangluo, shangqiu, shangrao, shangyu, shannan, shantou, shanwei, shaoguan, shaoxing, shaoyang, shenyang, shenzhen, shihezi, shijiazhuang, shishi, shiyan, shizuishan, shouguang, shuangyashan, shunde, shuozhou, siping, songyuan, suihua, suining, suizhou, suqian, suzhou, suzhou1, tacheng, taian, taicang, taiyuan, taizhou, taizhoux, tanggu, tangshan, tianchang, tianjin, tianshui, tieling, tongcheng, tongchuan, tonghua, tongliao, tongling, tonglu, tongren, tongxiang, tulufan, tunchang, wanning, weifang, weihai, weinan, wenchang, wenling, wenshan, wenzhou,wuhai, wuhan, wuhu, wujiang, wulanchabu, wulumuqi, wuwei, wuxi, wuyishan, wuyuan, wuzhen, wuzhishan, wuzhong, wuzhou, xiamen, xian, xiangfan, xianggang, xiangshan, xiangtan, xiangxi, xiangyang, xianning, xiantao, xianyang, xiaogan, xiaoshan, xichang, xilinguole, xingan, xingtai, xingyang, xining, xinmi, xinxiang, xinyang, xinyu, xinzheng, xishuangbanna, xuancheng, xuchang, xuzhou, yaan, yanan, yanbian, yancheng, yangjiang, yangquan, yangshuo, yangzhou, yanji, yanliang, yantai, yanzhou, yibin, yichang, yichun, yichun1, yili, yinchuan, yingkou, yingtan, yiwu, yixing, yiyang, yizheng, yongkang, yongzhou, yueyang, yuhang, yulin, yulin1, yuncheng, yunfu, yushu, yuxi, yuyao, zaozhuang, zhangjiagang, zhangjiajie, zhangjiakou, zhangye, zhangzhou, zhanjiang, zhaoqing, zhaotong, zhengzhou, zhenjiang, zhongshan, zhongwei, zhoukou, zhoushan, zhuhai, zhuji, zhumadian, zhuozhou, zhuzhou, zibo, zigong, ziyang, zunyi"
cities = cities.split(",")
city_chart = ["a"]


class NuomiSpider(scrapy.Spider):
    name = "nuomi"
    allowed_domains = ["nuomi.com"]
    start_urls = []
    url = "http://api.nuomi.com/api/dailydeal?version=v1"
    urlparam = ""
    for city in cities:
        city = city.strip()
        if city[0] in city_chart:
            urlparam += "&city=" + city
        else:
            start_urls.append(
                'http://api.nuomi.com/api/dailydeal?version=v1' + urlparam
            )
            urlparam = "&city=" + city
            city_chart.append(city[0])

    # def start_requests(self):
    # for url in self.start_urls:
    #         data = json.loads(response.body_as_unicode())
    #         body = json.dumps({"url": url, "wait": 0.5})
    #         headers = Headers({'Content-Type': 'application/json','User-Agent': user_agent})
    #         request= scrapy.Request(RENDER_HTML_URL, self.parse, method="POST",
    #                              body=body, headers=headers)
    #        request.meta['item'] = item 抓取图片时可以动态传入
    #          yield request
    # def parse(self, response):
    #
    #         yield  response.meta['item']



    def parse(self, response):
        dom = minidom.parseString(response.body)
        root = dom.documentElement
        roots = get_xmlnode(root, 'url')
        for root in roots:
            url = get_xmlnode(root, 'loc')[0].childNodes[0].nodeValue
            item = {"site": "nuomi", "shops": [], "url": url, "apiType": "hao123"}
            display_nodes = get_xmlnode(root, 'display')[0].childNodes
            for display in display_nodes:
                if display.nodeName == "#text":
                    continue
                elif display.nodeName == "shops":
                    shop_nodes = get_xmlnode(display, 'shop')
                    shop = {}
                    for shop_node in shop_nodes:
                        for node in shop_node.childNodes:
                            if node.nodeName == "#text":
                                continue
                            elif node.childNodes:
                                shop[node.nodeName] = node.childNodes[0].nodeValue  # wholeText
                    item["shops"].append(shop)
                elif display.childNodes:
                    name = display.nodeName
                    item[name] = display.childNodes[0].nodeValue  # wholeText
                    if name == "identifier":
                        item["id"] = item[name]
            yield item
