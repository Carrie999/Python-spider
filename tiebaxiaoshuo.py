import requests
import time
from bs4 import BeautifulSoup
'''
抓取百度贴吧---言情小说的基本内容
爬虫线路： requests - bs4
Python版本： 3.6
'''
import requests
import time
from bs4 import BeautifulSoup

def get_html(url):
    
    r = requests.get(url,timeout=30)
    r.raise_for_status()
    
    r.encoding = 'utf-8'
    return r.text
    
    
    
def get_content(url):
    comments = []
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    liTags = soup.find_all('li', attrs={'class': ' j_thread_list clearfix'})
    
    i=0
    for li in liTags:
        i+=1
        print(i)
        comment = {}
        
        comment['title'] = li.find('a', attrs={'class': 'j_th_tit '}).text.strip()
       
       
        print(comment['title'] )
        comments.append(comment)
        
    return comments
    
def OutFile(dict):
    with open('TTBT.txt', 'a+') as f:
        i=0
        i+=1
        for cc in dict:
            f.write( '1： {} \n'.format(cc['title']))
            print(333333)
        print('当前页面爬取完成')
def main(base_url, deep):
    url_list = []
    # 将所有需要爬去的url存入列表
    for i in range(0, deep):
        url_list.append(base_url + '&pn=' + str(50 * i))
    print('所有的网页已经下载到本地！ 开始筛选信息。。。。')

    #循环写入所有的数据
    for url in url_list:
        content = get_content(url)
        print(2222)
        print(content)
        OutFile(content)
    print('所有的信息都已经保存完毕！')
base_url = 'https://tieba.baidu.com/f?ie=utf-8&kw=%E8%A8%80%E6%83%85%E5%B0%8F%E8%AF%B4&fr=search'
deep = 2
if __name__ == '__main__':
    main(base_url, deep)
