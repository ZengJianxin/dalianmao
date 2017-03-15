HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
    }


class Options:

    def __init__(self, name, start_urls,
                 allow_redirects=True,
                 concurrence = 15, 
                 cookies=None,
                 debug=False,
                 db='mongodb',
                 db_settings=None,
                 deny=None,
                 dynamic=False,
                 headers=None,
                 magic=2,
                 max_redirects=10,
                 max_retry=5,
                 timeout=3*60
                ):
        '''
            name: str
            start_urls: list
            db_setting: dict
            denied: list
            cookies: dict
            headers: dict
        ''' 
        self.allow_redirects = allow_redirects
        self.concurrence = concurrence
        self.cookies = cookies
        self.db = db.lower()
        self.db_name = name
        self.db_settings = db_settings if db_settings else {}
        self.debug = debug
        self.deny = deny if deny else []
        self.dynamic = dynamic
        self.filename = name
        self.headers = headers if headers else HEADERS
        self.magic = magic
        self.max_redirects = max_redirects
        self.max_retry = max_retry
        self.start_urls = start_urls
        self.timeout = timeout
