import scrapy
import re
import time
from scrapy.utils.project import get_project_settings
from B_search.items import BSearchItem
import pandas as pd


#  B站弹幕的格式以及内容
#  https://www.bilibili.com/read/cv5187469/?from=readlist

class GetDanmuMachine(scrapy.Spider):
    name = 'get_danmu'
    kv = {"User-Agent":
              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
          }

    def start_requests(self):
        setting = get_project_settings()
        if not setting.get('SCRAPY_UP'):
            bv_number = setting.get('BV_NUMBER')
            if not isinstance(bv_number, list):
                url = 'https://www.bilibili.com/video/' + bv_number
                yield scrapy.Request(url, headers=self.kv)
            else:
                for bv_single_number in bv_number:
                    url = 'https://www.bilibili.com/video/' + bv_single_number
                    yield scrapy.Request(url, headers=self.kv)
        else:
            data = pd.read_csv('result_bv.csv', header=None, names=['BV'])
            bv_number_list = list(data.iloc[1:-1, 0])
            page = 1
            for bv_number in bv_number_list:
                url = 'https://www.bilibili.com/video/' + bv_number
                print('开始爬取第' + str(page) + '个视频的弹幕')
                page += 1
                yield scrapy.Request(url, headers=self.kv)

    def parse(self, response):
        if not response.xpath('//div[@class="head-con"]'):
            cid = re.findall(r'"pages":\[{"cid":(\d+)', response.text, re.S)
            cid_url = "https://comment.bilibili.com/{}.xml".format(cid[0])
            yield scrapy.Request(cid_url, callback=self.parse_get, headers=self.kv)
        else:
            cid = re.findall(r'{"cid":(\d+),"page":\d+', response.text, re.S)
            for i in cid:
                cid_url = "https://comment.bilibili.com/{}.xml".format(i)
                yield scrapy.Request(cid_url, callback=self.parse_get, headers=self.kv)

    def parse_get(self, response):
        item = BSearchItem()
        danmu_contents = response.xpath("//d")
        for danmu in danmu_contents:
            item["CONTENT"] = danmu.xpath("text()").extract()[0]
            danmu_info = danmu.xpath("@p").extract()[0].split(',')
            sending_time_standard = time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(int(danmu_info[4])))
            item["SENDING_TIME"] = sending_time_standard
            item["UID"] = danmu_info[-1]
            yield item
