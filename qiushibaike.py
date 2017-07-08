'''doc.抓取糗事百科热门段子'''
import requests
import time
from bs4 import BeautifulSoup
def get_html(url):
	try:
		r = requests.get(url, timeout=30)
		r.raise_for_status()
		r.encoding = 'utf-8'
		print (r.text)
		return r.text
	except:
		return " ERROR "
def get_content(url): 
	comments = []
	html = get_html(url)
	soup = BeautifulSoup(html, 'lxml')
	divs = soup.find_all('div', attrs={'class': 'content'})
	print (divs)
	for div in divs:  
		com=div.find('span',).get_text("\n")
		print(com)
		comments.append(com)
		
	return comments
def Out2File(list):
	with open('xh.txt', 'a+') as f:
		i=0
		for comment in list:
			i+=1
			f.write(str(i))
			f.write(comment)
			f.write("\n")
		print('当前页面爬取完成')
def main(base_url,deep):
	url_list = []
	for i in range(1, deep):
		url_list.append(base_url + str(i) + '/?s=4987646')
            
	for url in url_list:
		content = get_content(url)
		print(content)
		Out2File(content)
base_url = 'http://www.qiushibaike.com/hot/page/'
deep=3
if __name__ == '__main__':
	main(base_url,deep)
