# lianjiahangzhou
lianjiahangzhou-scrapy
用于爬取链家中杭州的数据

> 需要先安装mongodb，并启动服务器，如果有mongodb的server，可以修改storemongo.py中的连接

## 爬取楼盘数据
```
scrapy crawl hzloupan
```

## 爬取小区数据
```
scrapy crawl hzxiaoqu
```

## 爬取成交记录
```
scrapy crawl hzchengjiao
```
