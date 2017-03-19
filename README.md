# DaLianMao

Please fogive my poor English....

DaLianMao is a web crawling and web scraping microframework writen with Python 3.5+ coroutines, that means your spiders run asyncronously. It use a router to mannage the data streams when crawling websites, which makes its syntax Flask-like.

In Chinese, DaLianMao means a big faced cat, it comes from a very famous Chinese cartoon [蓝皮鼠和大脸猫 (The Blue Mouse and the Big Faced Cat)](https://en.wikipedia.org/wiki/The_Blue_Mouse_and_the_Big_Faced_Cat).

It's developed [on Github](<https://github.com/ZengJianxin/dalianmao>), contributions are welcome!


## Requirements

* Python 3.5+
* aiohttp, aiofiles, BeautifulSoup, Motor, optional: uvloop
* MongoDB, Splash if Options.dynamic is set to be True


## Installation

* pip install dalianmao


## Tutorial

### 1. Whetting Your Appetite
The program below is written to extract blog articles on [Github blog](https://github.com/blog).

github_blog.py

```python
    from dalianmao import Options, DaLianMao

    options_kargs = {'name': 'github_blog',
        'start_urls': ['https://github.com/blog',],
        'db_settings': {},
        'concurrence': 3,
        'magic': 5,
        }
    options = Options(**options_kargs)    # Options object
    app = DaLianMao(options)    # Create a spider

    # specify parse function to specific URLs,
    # a parse function should return a list of dicts or None 
    @app.route(r'https://github\.com/blog(\?page=\d+)?')
    async def only_follow(url, soup):

        return None

    # follow url_regex and extract data,
    # the __name__ of this function is used as the name of the collection
    # that stores the data it returned.
    @app.route(r'https://github\.com/blog/[0-9]+-[A-z0-9-]+')
    async def blog(url, soup):    # soup is a BeautifulSoup object
        data = []
        blog_title = soup.find('a', class_='blog-title')
        title = blog_title.text
        url = blog_title['href']
        blog_post_meta = soup.find('ul', class_='blog-post-meta').find_all('li')
        date = blog_post_meta[0].text
        author = blog_post_meta[1].text
        content = soup.find('div', class_='blog-post-body').text
        feedback = soup.find('div', class_='blog-feedback').text
        datum = {'title': title,
            'url': url,
            'date': date,
            'author': author,
            'content': content,
            'feedback': feedback
        }
        data.append(datum)
        return data    # return a list of data
    app.crawl()    # start crawling
```

Save the code as 'github_blog.py' and run with 'python github_blog.py' in your terminal. More examples can be found at [dalianmao/examples](https://github.com/ZengJianxin/dalianmao/tree/master/examples)

### 2. Options
* *name: str* -- name of the spider and the related database.
* *start_urls: list* -- the crawl started by making requests to the URLs defined in the start_urls
* *allow_redirects: boolean (default: True)* -- follow redirects?
* *concurrence: int (default: 15)* -- number of workers.
* *cookies: dict (default: None)* -- cookies to send with requests.
* *debug: boolean (default: False)* -- is debugging? if set to be True, log infos will print to terminal.
* *db: str (default: 'mongodb')* -- database used to store extracted data. currently, only mongodb is available.
* *db_settings: dict (default: {})* -- e.g. {'host': 'localhost', 'port': 27017}, the host parameter can be a full mongodb URI
* *deny: list (default: list)* -- list of urls(regular expression) that will not request.
* *dynamic: boolean (default: False)* -- run javascripts?
* *headers: dict (default: check in dalianmao/options.py)* -- HTTP headers to send with requests.
* *magic: int (default: 2)* -- time.sleep(magic*random.random()) between two ajacent requests, disabled if proxy is used.
* *max_redirects: int (default: 10)* -- max redirects.
* *max_retry: int (default: 5)* -- max retry if failed on requesting.
* *timeout: int (default: 3*60)* -- timeout in seconds for requesting.

### 3. Routing
Routing allows the user to specify parse function for different urls.

A basic route looks like following:
```python
    @app.route(url_regex)
    async def test(url, soup)
        ....
        return data
```
* When a url is passed to the router, it will check the route(url_regex) from up to bottom in the spider the user write and returns the first that matches, then the workers will requests the url with the parameters specified in the route, parse the webpage with the parse function in the route, and at last, returns the data.
* URLs that do not match any route in the spider will not be followed.
* The \__name__ of a route's parse function is used as the name of the collection(MongoDB) that stores the data it returns.
* The 'Referer' for requesting 'http://abc.cn/d/e/f' is set to be 'http://abc.cn/d/e'.
* The app.route decorator is a wrapper for app.add_route(self, handler, url, json=False, extract_urls = None, js_source=None) method.

### 4. Downloading Files and Pictures
```python
    ....

    @app.route(url_regex)
    async def test(url, soup):
        ....
        filename = await app.download(href, path, filename, referer=url)
        ...
        return data

    ....
```

### 5. Executor
```python
    from functools import partial

    from dalianmao import DaLianMao, Executor, Options

    executor = Executor()
    ....

    def func(test):
        ....
        return results

    @app.route(url_regex)
    assync def executor(url, soups):
       results = await app.run_in_executor(executor, partial(test, 'test'))
       ....
       return data

    ....

    app.crawl()
    executor.shutdown()
```

### 6. Run JavaScript
```python
    ....
    options = Options(...., dynamic=True)
    ....
    js_source = '....'

    @app.route(url_regex, js_source=js_source)
    async def test(url, soup):
        ....
        return data

    ....
```

### 7. Custom URLs Extractor
```python
    ....
    def urls_extractor(soup):
        ....
        return urls

    @app.route(url_regex, extract_urls=urls_extractor)
    async def test(url, soup):
        ....
        return data
    ....
```

### 8. Proxy Handler
```python
    ....

    def proxy_handler():
        with open('proxy.txt', 'r') as f:
            proxy = f.read().split('\r\n')
        return proxy

    ....
    app.add_proxy_handler(proxy_handler)
    ....
```

### 9. Parse JSON Response Content
```python
    ....

    @app.route(url_regex, json=True)
    async def test(url, soup):
        ....
        return data

    ....
```
