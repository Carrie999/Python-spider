'''
爬取各类小说排行榜，并保存为文件
使用 requests --- bs4 线路
Python版本： 3.6
'''
import requests
import bs4
def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.encoding = 'utf-8'
        return r.text
    except:
        return "Someting Wrong！"
def get_content(url):
    '''
    爬取每一类型小说排行榜，
    按顺序写入文件，
    文件内容为 小说名字+小说链接
    将内容保存到列表
    并且返回一个装满url链接的列表
    '''
    url_list = []
    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')
    # 由于小说排版的原因，历史类和完本类小说不在一个div里
    category_list = soup.find_all('div', class_='index_toplist mright mbottom')
    history_finished_list = soup.find_all('div', class_='index_toplist mbottom')
    for cate in category_list:
        name = cate.find('div', class_='toptab').span.string
        with open('novel_list.txt', 'a+') as f:
            f.write("\n小说种类：{} \n".format(name))
            # 我们直接通过style属性来定位总排行榜
        general_list = cate.find(style='display: block;')
        # 找到全部的小说名字，发现他们全部都包含在li标签之中
        book_list = general_list.find_all('li')
    # 循环遍历出每一个小说的的名字，以及链接
    for book in book_list:
        link = 'http://www.qu.la/' + book.a['href']
        title = book.a['title']
        # 我们将所有文章的url地址保存在一个列表变量里
        url_list.append(link)
        # 这里使用a模式，防止清空文件
        with open('novel_list.txt', 'a') as f:
            f.write("小说名：{} \t 小说地址：{} \n".format(title, link))
    for cate in history_finished_list:
        name = cate.find('div', class_='toptab').span.string
        with open('novel_list.csv', 'a') as f:
            f.write("\n小说种类：{} \n".format(name))
        general_list = cate.find(style='display: block;')
        book_list = general_list.find_all('li')
    for book in book_list:
        link = 'http://www.qu.la/' + book.a['href']
        title = book.a['title']
        url_list.append(link)
        with open('novel_list.csv', 'a') as f:
            f.write("小说名：{:<} \t 小说地址：{:<} \n".format(title, link))
    return url_list
def get_txt_url(url):
    '''
    获取该小说每个章节的url地址：
    并创建小说文件
    '''
    url_list2 = []
    html = get_html(url)
    soup = bs4.BeautifulSoup(html, 'lxml')
    lista = soup.find_all('dd')
    txt_name = soup.find('h1').text
    with open('小说/{}.txt'.format(txt_name), "a+") as f:
        f.write('小说标题：{} \n'.format(txt_name))
    for url in lista:
        url_list2.append('http://www.qu.la/' + url.a['href'])
    return url_list2, txt_name
    #每个章节的url和小说名
def get_one_txt(url, txt_name):
    '''
    获取小说每个章节的文本
    并写入到本地
    '''
    html = get_html(url).replace('<br/>', '\n')
    
    soup = bs4.BeautifulSoup(html, 'lxml')
    try:
        txt = soup.find('div', id='content').text.replace('chaptererror();', '')
        print(txt)
        txt = ''.join(txt.split())
        title = soup.find('title').text
        print(title)
        with open('小说/{}.txt'.format(txt_name), "a+") as f:
            f.write(title + '\n\n')
            f.write(txt + '\n\n')
        print('当前小说：{} 当前章节{} 已经下载完毕'.format(txt_name, title))
    except:
        print('someting wrong')
def get_all_txt(url_list):
    '''
    下载排行榜里所有的小说
    并保存为txt格式
    '''
    #url_list 30章的url   



    for url in url_list:
        # 便利获取当前小说的所有章节的目录，
        # 并且生成小说头文件
        page_list, txt_name = get_txt_url(url)
        
        for page_url in page_list:
        # 遍历每一篇小说，并下载到目录
            get_one_txt(page_url, txt_name)
            print (len(url_list)) 
            print('整体当前进度 {}% '.format((url_list.index(url)+1) / len(url_list) * 100))
            print('当前小说进度 {}% '.format((page_list.index(page_url)+1) / len(page_list) * 100))
    
def main():
    # 排行榜地址：
    url = 'http://www.qu.la/paihangbang/'
    # 获取排行榜中所有小说的url连接
    url_list = get_content(url)
    # 除去重复的小说，增加效率
    url_list = list(set(url_list))
    get_all_txt(url_list)
if __name__ == '__main__':
    main()
