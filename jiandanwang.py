import urllib.request
import os
import random

def url_open(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.71 Safari/537.36')

    proxies = ['110.73.30.246:6666','121.31.199.91:6675','124.132.83.173:6675']
    proxy =random.choice(proxies)

    proxy_support=urllib.request.ProxyHandler({'http':proxy})
    opener =urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)
    
    response = urllib.request.urlopen(url)
    html = response.read()
    return html


def get_page(url):
    html = url_open(url).decode('utf-8')
    a= html.find('current-comment-page')+23
    b=html.find(']',a)
    print(html[a:b])
    return html[a:b]
    
def find_img(url):
    html = url_open(url).decode('utf-8')
    img_addrs = []
    a =html.find('img src=')
    
    while a!=-1:
        
        b =html.find('.jpg',a,a+255)

        if b!= -1:
            img_addrs.append(html[a+9:b+4])
        else:
            b= a+9
        a =html.find('img src=',b)
    print(img_addrs[2:])
    return img_addrs
        
def save_img(folder,img_addrs):
    for each in img_addrs:
        filename=each.split('/')[-1]
        print(each[0:4])
        with open(filename,'wb') as f:
            if each[0:4] == 'http':
                img=url_open(each)
                print(1)
            else:
                img=url_open('http:'+each)
                print(2)
                f.write(img)

def download_mm(folder='drawings',pages=10):
    
    os.chdir(folder)

    url ="http://jandan.net/drawings/"
    page_num = int(get_page(url))
    
    for i in range(pages):
        page_num -= i
        page_url = url + 'page-' + str(page_num)  + '#comments'
        img_addrs = find_img(page_url)
        save_img(folder,img_addrs)

if __name__ == '__main__':
    download_mm()
   
