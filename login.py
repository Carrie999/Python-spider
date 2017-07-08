# -*- coding: utf8 -*-
import urllib2
import urllib
import cookielib
import re
import bs4
URL_BAIDU_INDEX = u'http://www.baidu.com/'
#https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=true 也可以用这个
URL_BAIDU_TOKEN = 'https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3&class=login'
URL_BAIDU_LOGIN = 'https://passport.baidu.com/v2/api/?login'
#设置用户名、密码
username = '15131211873'
password = '*******'
#设置cookie，这里cookiejar可自动管理，无需手动指定
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
reqReturn = urllib2.urlopen(URL_BAIDU_INDEX)
#获取token
tokenReturn = urllib2.urlopen(URL_BAIDU_TOKEN)
matchVal = re.search(u'"token" : "(?P<tokenVal>.*?)"',tokenReturn.read())
tokenVal = matchVal.group('tokenVal')
#构造登录请求参数，该请求数据是通过抓包获得，对应https://passport.baidu.com/v2/api/?login请求
postData = {
'username' : username,
'password' : password,
'u' : 'https://passport.baidu.com/',
'tpl' : 'pp',
'token' : tokenVal,
'staticpage' : 'https://passport.baidu.com/static/passpc-account/html/v3Jump.html',
'isPhone' : 'false',
'charset' : 'UTF-8',
'callback' : 'parent.bd__pcbs__ra48vi'
}
postData = urllib.urlencode(postData);
#发送登录请求
loginRequest = urllib2.Request(URL_BAIDU_LOGIN,postData)
loginRequest.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
loginRequest.add_header('Accept-Encoding','gzip,deflate,sdch')
loginRequest.add_header('Accept-Language','zh-CN,zh;q=0.8')
loginRequest.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36')
loginRequest.add_header('Content-Type','application/x-www-form-urlencoded')
sendPost = urllib2.urlopen(loginRequest)
#查看贴吧个人主页 ，测试是否登陆成功，由于cookie自动管理，这里处理起来方便很多
#http://tieba.baidu.com/home/main?un=XXXX&fr=index 这个是贴吧个人主页，各项信息都可以在此找到链接
teibaUrl = 'http://tieba.baidu.com/f/like/mylike?v=1387441831248'
content = urllib2.urlopen(teibaUrl).read()
content = content.decode('gbk').encode('utf8')
print content
#解析数据，用的BeautifulSoup4
soup = bs4.BeautifulSoup(content)
list = soup.findAll('tr')
list = list[1:len(list)]
careTeibalist = []
print '贴吧链接\\t吧名\\t等级'
for elem in list:
    soup1 = bs4.BeautifulSoup(str(elem))
    print 'http://tieba.baidu.com/'+soup1.find('a')['href']+'\\t'+soup1.find('a')
