# -*- coding: utf-8 -*-
from selenium import webdriver
url = 'https://www.baidu.com'
browser = webdriver.PhantomJS()
browser.get(url)
browser.implicitly_wait(2)
text = browser.find_element_by_id('kw')
text.send_keys('python')
button = browser.find_element_by_id('su')
button.submit()
results = browser.find_elements_by_class_name('t')
print(results)
print(browser.title)
for result in results:
    print('标题：{} \n超链接：{}'.format(result.text,result.find_element_by_tag_name('a').get_attribute('href')))
