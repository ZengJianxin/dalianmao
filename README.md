# 大脸猫
大脸猫是一个基于aiohttp，uvloop和BeautifulSoup的爬虫框架，框架结构类似Scrapy，语法类似Flask 
(多进程和分布式版本暂定名为“蓝皮鼠”，等写完毕业论文并找到工作后再写)
## 依赖
该框架依赖于uvloop，aiohttp，aiofiles，Motor，BeautifulSoup等非python标准库，使用前应确保安装，pip可以自动安装
## 安装
* pip install dalianmao
* 下载源码后用 python setup.py 安装
## 使用
大脸猫爬虫框架的__init__.py引入了三个类：Executor，Options，和DaLianMao
* Executor为标准库concurrent.futures中的ProcessPoolExecutor
* Options为配置文件，可以设置爬虫名字name: str，初始链接start_urls: list，这两个设置项是Options初始化
必须指明的，如：
options = Options(name='wandoujia', start_urls=['http://www.wandoujia.com/apps', ])其它缺省项将在后面详述
