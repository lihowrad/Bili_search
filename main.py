# -*- coding: utf-8 -*-
import os
from scrapy.utils.project import get_project_settings
from time import sleep

settings = get_project_settings()
print('程序开始运行')
sleep(2)
if settings.get('SCRAPY_UP'):
    print('开始对一个up主的弹幕情况进行分析')
    sleep(2)
    print('开始抓取up主所有视频的bv号, 并保存结果于result_bv.csv')
    print('运行get_people_bv.py')
    sleep(2)
    os.system('python B_analyze/get_people_bv.py')
    print('开始抓取视频中的弹幕')
    print('运行爬虫get_danmu, 并保存结果于result.csv')
    sleep(2)
    os.system('scrapy crawl get_danmu -o result.csv')
    print('爬取结束')
    sleep(1)
    print('开始分析弹幕的高频词')
    print('运行danmu_extract.py, 并保存结果于result_keywords.csv')
    sleep(2)
    os.system('python B_analyze/danmu_extract.py')
    print('分析结束')
    sleep(2)
    print('程序执行完成')