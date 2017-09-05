# -*- coding: utf-8 -*-
#这个用到了
import json

import requests
from pyquery import PyQuery as pq
from requests.exceptions import ConnectionError
from config import *  #import *之后，就可以引用config中的所有变量
import pymongo

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
start_url = 'http://www.dy2018.com/0/'
origin_url = 'http://www.dy2018.com/'



def get_second_page(url):
    for i in range(20):
        second_url = origin_url + str(i)
        #print(second_url[:-2])
        get_third_page(second_url)


def get_third_page(url):
    #需要加异常处理
    try:
        response = requests.get(url, headers = headers)
        response.encoding = 'gb2312'
        doc = pq(response.text) #pyquery解析.
        page_numbers = doc.find('option').items()  #不能在find_all得到的内容后直接获取属性，因为是在列表内
        #print(page_numbers)
        for page_number in page_numbers:
            #print(page_number.attr('value'))
            third_url = url + page_number.attr('value')[2:]
            #print(third_url)
            get_index_page(third_url)
        return None
    except ConnectionError:
        return '连接不上了1'


def get_index_page(url):
    try:
        response = requests.get(url, headers = headers)
        #print(response.apparent_encoding)                  #获取网页编码格式，下一句解决中文乱码问题
        response.encoding = 'gb2312'
        if response.status_code == 200:
            #print(response.text)
            doc = pq(response.text)     #不需要解析器
            lists = doc.find('.co_content8 ul table').items()
            for list in lists:
                href = origin_url + list.find('a').eq(1).attr('href')[1:]
                score = list.find('font').eq(1).text()[5:]
                name = list.find('a').eq(1).attr('title')
                get_download_url(href, name, score)
                # info = {
                #     'name' : list.find('a').eq(1).attr('title'),
                #     'score' : list.find('font').eq(1).text()[5:],
                #     'download' : get_download_url(href)
                # }
                #print(info)

        else:
            return response.status_code
        return None
    except ConnectionError:
        return '列表页连接出错'

#解析单个电影，获得下载地址
def get_download_url(url, title, point):
    try:
        if point > '8':
            response = requests.get(url, headers = headers)
            response.encoding = 'gb2312'
            doc = pq(response.text)
            down_url = doc('#Zoom tbody a').text()
            info = {
                'movie_name': title,
                'movie_score': point,
                'movie_url': down_url
            }
            #save_to_mongo(info)
            save_to_text(info)
            #print(down_url)
            #return down_url
    except ConnectionError:
        return '详情页出错'

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到MONGO成功',result)
    except Exception:
        print('存储到MONGODB失败',result)

def save_to_text(result):
    with open('movie1.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False) + '\n')
        f.close()


def main():
    get_second_page(origin_url)
    #get_index_page(start_url)
    #get_download_url(test_url)


if __name__ == '__main__':
    main()