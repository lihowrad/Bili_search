# -*- coding: utf-8 -*-
from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from scrapy.utils.project import get_project_settings
import re
from time import sleep
import pandas as pd


def get_bv_numbers(browsers):
    """
    抓取当前页面上所有的视频bv号
    :param browsers: selenium 的 webdriver.Chrome实例
    :return: bv号的列表
    """
    print('正在匹配bv号')
    hrefs_bv = browsers.find_elements_by_xpath('//div[@class="title-row"]/a')
    bv_number_list = []
    if hrefs_bv:
        print('已经匹配到数据')
        for href_bv in hrefs_bv:
            bv_url = href_bv.get_attribute('href')
            bv_number = re.findall(r'https://www.bilibili.com/video/(\w*)', bv_url)[0]
            # print('提取bv号' + bv_number)
            bv_number_list.append(bv_number)
        print('已经提取完所有bv号')
    else:
        print('未匹配到数据')
    return bv_number_list


if __name__ == '__main__':
    bv_numbers = []
    settings = get_project_settings()
    print('开始查找该up主的所有视频bv号')
    print('正在打开浏览器')
    option = webdriver.ChromeOptions()
    option.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"')
    option.add_argument('--headless')
    option.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=option)
    page = 1
    tmp_list = [1]
    while tmp_list:
        print('这是第' + str(page) + '页')
        browser.get('https://space.bilibili.com/'+settings.get('UID')+'/video?tid=0&page=' + str(page) + '&keyword=&order=pubdate')
        sleep(2)
        tmp_list = get_bv_numbers(browser)
        bv_numbers = bv_numbers + tmp_list
        page += 1
    print('爬取结束')
    browser.quit()
    print('开始写入结果')
    results_bv = 'result_bv.csv'
    data = pd.DataFrame({"BV号": bv_numbers})
    data.to_csv(results_bv, index=False)
    print('结果成功写入,保存在' + results_bv)








