from dalianmao import Executor, Options, DaLianMao

options_kargs = {'name': 'github_blog',
    'start_urls': ['https://github.com/blog',],
    'concurrence': 3,
    'magic': 3,
}
options = Options(**options_kargs)
app = DaLianMao(options)

@app.route(r'https://github\.com/blog(\?page=\d+)?')
async def only_follow(url, soup):

    return None

@app.route(r'https://github\.com/blog/[0-9]+-[A-z0-9-]+')
async def blog(url, soup):
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
    return data

app.crawl()
