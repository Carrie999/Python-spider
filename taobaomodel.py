# -*- coding:utf-8 -*-
'''
抓取https://mm.taobao.com/json/request_top_list.htm?page=1
淘宝MM的头像地址，MM姓名，MM年龄，MM居住地，以及MM的个人详情页面地址
保存
'''
import urllib.request
import requests
import time
import re
import os
from bs4 import BeautifulSoup

siteURL = 'http://mm.taobao.com/json/request_top_list.htm'
#获取html页
def get_html(pageIndex):
    url = siteURL + "?page=" + str(pageIndex)
    r = requests.get(url,timeout=30)
    r.encoding = 'gbk'
    return r.text
#获取mm头像地址，mm详情地址，mm名字，mm年龄，mm居住地
def get_content(pageIndex):
    html = get_html(pageIndex)
    pattern = re.compile('<div class="pic-word".*?<img src="(.*?)".*?<a class="lady-name" href="(.*?)".*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',re.S)
    items = re.findall(pattern,html)
    contents = []
    for item in items:
        contents.append([item[0],item[1],item[2],item[3],item[4]])
    return contents
#获取个人详情页面
def getDetailPage(infoURL):
    r = requests.get('http:'+infoURL)
    r.encoding = 'gbk'
    return r.text
#获取页面所有图片
def getAllImg():
    page=get_html(https://mm.taobao.com/self/album/open_album_list.htm?_charset=utf-8&user_id%20=687471686)
    patternImg = re.compile('<img.*src="(.*?)"',re.S)
    print(page)
    images = re.findall(patternImg,page)
    print (images)
    return images
#保存多张写真图片
def saveImgs(images,name):
    number = 1
    print (u"发现",name,u"共有",len(images),u"张照片")
    for imageURL in images:
        splitPath = imageURL.split('.')
        fTail = splitPath.pop()
        if len(fTail) > 3:
            fTail = "jpg"
        fileName = name + "/" + str(number) + "." + fTail
        saveImg('http:'+imageURL,fileName)
        number += 1
# 保存头像
def saveIcon(iconURL,name):
    splitPath = iconURL.split('.')
    fTail = splitPath.pop()
    fileName = name + "/icon." + fTail
    saveImg('http:'+iconURL,fileName)

#写入图片
def saveImg(imageURL,fileName):
    imageURL=imageURL.replace('			', '')
    print(imageURL)
    req = urllib.request.Request(imageURL)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.71 Safari/537.36')
    response = urllib.request.urlopen(imageURL)
    img = response.read()
    f = open(fileName, 'wb')
    f.write(img)
    f.close()
#写入文本
def saveBrief(content,name):
    fileName = name + "/" + name + ".txt"
    f = open(fileName,"w+")
    print (u"正在偷偷保存她的个人信息为",fileName)
    f.write(content.encode('utf-8'))
#创建新目录
def mkdir(path):
    path = path.strip()
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False
#将一页淘宝MM的信息保存起来      
def savePageInfo(pageIndex):
    contents = get_content(pageIndex)
    for item in contents:
        #item[0]头像URL,item[1]个人详情URL,item[2]姓名,item[3]年龄,item[4]居住地
        print (u"发现一位模特,名字叫",item[2],u"芳龄",item[3],u",她在",item[4])
        print (u"正在保存",item[2],"的信息")
        print (u"她的个人地址是",item[1])
        #个人详情页面的URL
        detailURL = item[1]
        #得到详情页图片
        detailPage = getDetailPage(detailURL)
        images = getAllImg(detailPage)
        #创建目录
        mkdir(item[2])
        #保存头像
        saveIcon(item[0],item[2])
        #保存详情页写真集
        saveImgs(images,item[2])
def savePagesInfo(start,end):
    for i in range(start,end+1):
        print (u"正在寻找第",i,u"个地方，看看MM们在不在")
        savePageInfo(i)

if __name__ == '__main__':
    savePagesInfo(1,2)   

