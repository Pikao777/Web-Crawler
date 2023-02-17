# 載入套件
import requests
from bs4 import BeautifulSoup
import pymysql
from pymysql.err import IntegrityError

# main
if __name__ == '__main__':
    
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    }
    prefix = 'https://udn.com'
    # 開關
    lock = 0
    # 每頁有6篇
    page = 0
    while page<=98:
        if lock == 0:
            url = 'https://udn.com/api/more?page=' + str(page) + '&channelId=2&type=cate_latest_news&cate_id=6645&totalRecNo=576'
            r = requests.get(url, headers=headers)
            info = r.json()
            # 內文爬取
            for i in range(6):
                # VIP文章無法閱讀所以要寫try except避免錯誤
                try:
                    content_url = prefix + info['lists'][i]['titleLink']
                    content_r = requests.get(content_url)
                    soup = BeautifulSoup(content_r.text, features='lxml')
                    context_author = soup.find('span',{'class':'article-content__author'})
                    content = soup.find('section',{'class':'article-content__editor'})

                    website = 'udn'
                    link = content_url
                    title = info['lists'][i]['title']
                    time = info['lists'][i]['time']['date']
                    author = context_author.text
                    context = content.text

                    # 新增進資料庫
                    connection = pymysql.connect(host='localhost', port=3306, user='root', password='Password', database='stock_news')
                    cursor = connection.cursor()
                    sql = 'INSERT INTO ss_news (news, link, title, times, reporter, article) VALUES ("%s", "%s", "%s", "%s", "%s", "%s");'\
                                        % (website, link, title, time, author, context)
                    cursor.execute(sql)
                    connection.commit()
                    connection.close()
                except IntegrityError as e:
                    # 如果出現IntegrityError，也就是PK重複
                    print('已經抓取到最新資料')
                    connection.close()
                    print('關閉資料庫連接')
                    lock = 1
                    break
                except Exception as e:
                    # 遇到VIP文章時要跳過
                    pass
            page += 1
        else:
            break