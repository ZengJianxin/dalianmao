import os.path

from dalianmao import DaLianMao, Options

app_icon_path = os.path.join(os.path.dirname(__file__), 'app-icon')
options = Options(name='s',
                  start_urls= ['http://www.wandoujia.com/apps', ],
                  concurrence=3
                 )
app = DaLianMao(options)

@app.route(r'http[s]?://www\.wandoujia\.com/apps/.+/comment[0-9]*(?<!html)$')
async def comments(url, soup):
    name = str(soup.select('#comments .block-title')[0].string).split(' ')[0].strip()
    comments_list = soup.select('.comments .comments-list li')
    comments = [list(comment.stripped_strings) for comment in comments_list]
    data = [{'name': name, 'comment': comment} for comment in comments]
    return data

@app.route(r'http[s]?://www\.wandoujia\.com/apps/[A-z0-9\.]+(?<!html)$')
async def apps(url, soup):
    filename = str(soup.select('.detail-top .app-info .title')[0].string).replace('/', '_')
    img_src = soup.select('.app-icon img')[0]['src']
    name = await app.download(img_src, app_icon_path, filename)
    install = int(soup.select('.num-list .item i[itemprop="interactionCount"]')[0]['content'].split(':')[-1].strip())
    like = int(str(soup.select('.num-list .item.love i')[0].string))
    comment = int(str(soup.select('.num-list .item.last i')[0].string))
    data = {'来源': url,
            '名称': name,
            '安装数': install,
            '喜欢数': like,
            '评论数': comment
            }
    infos = soup.find('dl', class_='infos-list')
    for dt, dd in zip(infos.find_all('dt'), infos.find_all('dd')):
        info = list(dd.stripped_strings)
        if len(info) == 0:
            info = None
        elif len(info) == 1:
            info = info[0]
        data[str(dt.string)] = info
    data['描述'] = '\n'.join(list(soup.select('.award-info .con, .change-info .con, .desc-info .con')[0].stripped_strings))
    return [data]

@app.route(r'http[s]?://www\.wandoujia\.com[A-z0-9\./]*(?<!html)$')
async def follow(url, soup):

    return None

app.crawl()
