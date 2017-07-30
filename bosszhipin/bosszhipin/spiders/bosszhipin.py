# -*- coding: utf-8 -*-
'''
boss直聘爬虫工程师的职位数据下载以及分析
使用本机scrapy—redis，代理ip
'''

import scrapy
from scrapy.http import Request
from bosszhipin.items import BosszhipinItem
from scrapy_redis.spiders import RedisSpider

class bosszhipinSpider(RedisSpider):
    name ="bosszhipin"
    #redis_key='bosszhipin:start_urls'
    urls=[]
    for i in range(1,9):
        aa="http://www.zhipin.com/c101010100/h_101010100/?query=%E7%88%AC%E8%99%AB&page=2&ka=page-"+str(i)
        urls.append(aa)
    start_urls = urls
    allowed_domains = ["www.zhipin.com"]

    def start_requests(self):
        for url in self.start_urls:
            print('开始爬')
            yield Request(url, self.parse)

    def parse(self, response):
        base_url ='http://www.zhipin.com'
        divs = response.xpath('//div[@class="job-primary"]')
        lis = response.xpath('//*[@id="main"]/div[3]/div[2]/ul/li')
        for li in lis:
            item = BosszhipinItem()
            item['name'] = li.xpath('./a/div[@class="job-primary"]/div[@class="info-primary"]/h3[@class="name"]/text()').extract()
            item['salary']= li.xpath('./a/div[@class="job-primary"]/div[@class="info-primary"]/h3[@class="name"]/span[@class="red"]/text()').extract()
            item['message']= li.xpath('./a/div[@class="job-primary"]/div[@class="info-primary"]/p/text()').extract()
            item['company_name']=li.xpath('./a/div[@class="job-primary"]/div[@class="info-company"]/div[@class="company-text"]/h3[@class="name"]/text()').extract()
            item['company_href']=str(li.xpath('./a/@href').extract())
            dd=item['company_href']
            details=base_url+dd[2:-2]
            #print(details)
            with open('zp.txt', 'a+') as f:
                f.write("{}\n".format(item))
            yield Request(details, callback=self.details,meta={'item2':item})
    def details(self, response):
        item = response.meta['item2']
        ee=response.xpath('//div[@class="text"]/text()').extract()
        ee =str(ee).replace("\\n","").replace(',', '').replace(' ', '').replace("'", '')
        item['requirement']=ee
        #print(item)
        return item
