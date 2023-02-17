#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# PTT論壇文章標題爬取-以八卦版為例

# 使用套件
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import re


def get_reply_info_list(url):
    # 爬取列表確認是否正確回傳http://localhost:8889/notebooks/Desktop/Github/Web-Crawler/ptt.ipynb#
    r = requests.get(url, headers=headers, cookies=cookies)
    if r.status_code != requests.codes.ok:
        print("載入失敗")
        return {}

def get_article_title(url):
    # 獲取文章標題
    elements = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(elements.text, "html.parser")
    element = soup.select('div.title a')
    for title in element:
        print(title.text)
    
def get_final_page():
    # 獲取最後一頁頁數
    elements = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(elements.text, "html.parser")
    href_tag = soup.select("a.wide") #搜尋最後頁數用  
    page_href = href_tag[-3].get('href') #找出tag標籤
    page = re.sub("/bbs/Gossiping/index","",page_href) #去除頁數前後文字
    final_page = re.sub(".html","",page) #同上
    return int(final_page)+1

# main
if __name__ == '__main__':
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    }
    cookies = { "cookie": "ga=GA1.2.821944995.1661921213; _gid=GA1.2.1593752975.1662445811; over18=1; _gat=1" }
    url = "https://www.ptt.cc/bbs/Gossiping/index.html"
    if get_reply_info_list(url) == False:
        print('網頁載入失敗')
    else:
        page = get_final_page()
        num = 10 # 設定要爬取的頁面數
        while num > 0:
            get_article_title('https://www.ptt.cc/bbs/Gossiping/index'+str(page)+".html")
            page = page - 1
            num = num -1

