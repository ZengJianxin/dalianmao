# 大脸猫
大脸猫是一个基于aiohttp，uvloop和BeautifulSoup的爬虫框架，框架结构类似Scrapy，语法类似Flask，本框架目前限制速度的因素在于url去重算法，后续会使用Cython重写。 
(多进程和分布式版本暂定名为“蓝皮鼠”，等写完毕业论文并找到工作后再写)
## 依赖
该框架依赖于uvloop，aiohttp，aiofiles，Motor，BeautifulSoup等非python标准库，使用前应确保安装，pip可以自动安装<br>
若需要动态加载或运行自定义的js代码，需要先运行Splash
## 安装
* pip install dalianmao
* 下载源码后用 python setup.py install安装
## 使用
大脸猫爬虫框架的__init__.py引入了三个类：Executor，Options，和DaLianMao。在新建爬虫时，Options和DaLianMao必须引入<br>
from dalianmao import Options, DaLianMao
* Executor为标准库concurrent.futures中的ProcessPoolExecutor，可以通过DaLianMao.run_in_executor(Executor, func)使用，func如果带参数，可以使用functools.partial
* Options为配置文件，可以设置爬虫名字name: str，初始链接start_urls: list，这两个设置项是Options初始化
必须指明的，如：<br>
options = Options(name='wandoujia', start_urls=['http://www.wandoujia.com/apps', ])，
<br>其它缺省项将在后面详述
* 通过DaLianMao可以新建爬虫对象，使用时仅需传递Options对象<br>
app = DaLianMao(options)<br>
未完待续。。。有兴趣的朋友可以先看以下examples，虽然其中并没有用到本框架所有功能
