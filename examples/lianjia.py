import re

from dalianmao import DaLianMao, Options, utils

cityName = re.compile(r"(?<=cityName: ').*?(?=')")
city_name = re.compile(r"(?<=city_name: ').*?(?=')")
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11, Fedora, Linux x86_64, rv:51.0) Gecko/20100101 Firefox/51.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml,q=0.9,*/*,q=0.8',
    'Accept-Language': 'zh-CN,zh,q=0.8,en-US,q=0.5,en,q=0.3',
    #'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
    }
js_source = 'window.scrollTo(0, document.body.scrollHeight)'
cookies = 'lianjia_uuid=1956ef69-2f57-4849-89f2-f8a2f93e71f9; _smt_uid=58b635d7.55d3346b; _jzqa=1.609558669798200000.1488336343.1491487454.1491549165.56; _jzqy=1.1488336343.1489297752.2.jzqsr=baidu.jzqsr=baidu|jzqct=lianjiawang; _ga=GA1.2.1561746767.1488336345; gr_user_id=1b64c3d2-3af6-42a0-a580-1dadf1169fd3; ubta=2299869246.1536406642.1489032612362.1490920420189.1490920421144.5; UM_distinctid=15ac1103ffb37-08c9f6be1433d08-64257242-100200-15ac1103ffc420; _jzqx=1.1489314422.1491487454.5.jzqsr=captcha%2Elianjia%2Ecom|jzqct=/.jzqsr=hz%2Elianjia%2Ecom|jzqct=/ershoufang/pg100/; __xsptplus696=696.1.1490919685.1490920420.4%234%7C%7C%7C%7C%7C%23%23SnztPdR4n_EFpOrgRmxzbMkg8QScp86T%23; select_city=320100; lianjia_ssid=4ddd7a59-51b9-4727-b5da-df80807c6f31; _jzqb=1.4.10.1491549165.1; _jzqc=1; _jzqckmp=1; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1; all-lj=ae53ba2bb01d9055b48cc0081f0ce3f9; _qzja=1.939967435.1491549178813.1491549178813.1491549178813.1491549193157.1491549199664.0.0.0.3.1; _qzjb=1.1491549178813.3.0.0.0; _qzjc=1; _qzjto=3.1.0; CNZZDATA1253492138=1282769646-1491544645-http%253A%252F%252Fhz.lianjia.com%252F%7C1491544645; CNZZDATA1254525948=1478655530-1491547593-http%253A%252F%252Fhz.lianjia.com%252F%7C1491547593; CNZZDATA1255633284=1830259418-1491545275-http%253A%252F%252Fhz.lianjia.com%252F%7C1491545275; CNZZDATA1255604082=1766106234-1491545483-http%253A%252F%252Fhz.lianjia.com%252F%7C1491545483'
cookies = utils.cookiestring2dict(cookies)
city = '南京'
city_code = 'nj'

options = Options(name='lianjia',
                  start_urls= ['http://' + city_code + '.lianjia.com/', ],
                  headers=HEADERS,
                  dynamic=True,
                  concurrence=3,
                  magic=20,
                  cookies=cookies
                 )
app = DaLianMao(options)

@app.route(r'http://' + city_code + r'\.fang\.lianjia\.com/loupan/(pg[0-9]*/)?', js_source=js_source)
async def loupan(url, soup):
    data = []
    #try:
    #    city = cityName.search(str(soup)).group()
    #except:
    #    city = city_name.search(str(soup)).group()
    house_list = soup.find('ul', class_='house-lst').find_all('li')
    for house in house_list:
        info = house.find('div', class_='info-panel')
        if not info:
            continue
        try:
            col_1 = info.find('div', class_='col-1')
        except:
            print(house_list)
        title = str(col_1.h2.a.string)
        where = str(col_1.find('div', class_='where').span.string)
        area = ' '.join(list(col_1.find('div', class_='area').stripped_strings))
        other = list(col_1.find('div', class_='other').stripped_strings) if col_1.find('div', class_='other') else None
        type_ = list(col_1.find('div', class_='type').stripped_strings)
        col_2 = info.find('div', class_='col-2')
        average = ' '.join(list(col_2.find('div', class_='average').stripped_strings))
        tehui = ' '.join(list(col_2.find('div', class_='tehui').stripped_strings))
        pic_src = house.find('div', class_='pic-panel').find('img')['src']
        datum = {'city': city,
                'title': title,
                'where': where,
                'area': area,
                'other': other,
                'type': type_,
                'average': average,
                'tehui': tehui
                }
        data.append(datum)
    return data

@app.route(r'http://' + city_code + r'\.lianjia\.com/ershoufang/(pg[0-9]*/)?', js_source=js_source)
async def ershoufang(url, soup):
    data = []
    #try:
    #    city = cityName.search(str(soup)).group()
    #except:
    #    city = city_name.search(str(soup)).group()
    sell_list = soup.find('ul', class_='sellListContent').find_all('li')
    for sell in sell_list:
        info = sell.find('div', class_='info')
        if not info:
            continue
        title = str(info.find('div', class_='title').a.string)
        house_info = ' '.join(list(info.find('div', class_='address').stripped_strings))
        position_info = ' '.join(list(info.find('div', class_='flood').stripped_strings))
        follow_info = ' '.join(list(info.find('div', class_='followInfo').stripped_strings))
        tag = list(info.find('div', class_='tag').stripped_strings)
        total_price = ' '.join(list(info.find('div', class_='totalPrice').stripped_strings))
        datum = {'city': city,
                 'title': title,
                 'house-info': house_info,
                 'position-info': position_info,
                 'follow-info': follow_info,
                 'tag': tag,
                 'total-price': total_price
                 }
        data.append(datum)
    return data

@app.route(r'http://' + city_code + r'\.lianjia\.com/zufang/(pg[0-9]*/)?', js_source=js_source)
async def zufang(url, soup):
    data = []
    #try:
    #    city = cityName.search(str(soup)).group()
    #except:
    #    city = city_name.search(str(soup)).group()
    house_list = soup.find('ul', id='house-lst').find_all('li')
    for house in house_list:
        info = house.find('div', class_='info-panel')
        if not info:
            continue
        title = str(info.h2.a.string)
        col_1 = info.find('div', class_='col-1')
        where = ' '.join(list(col_1.find('div', class_='where').stripped_strings))
        other = ' '.join(list(col_1.find('div', class_='other').stripped_strings))
        chanquan = ' '.join(list(col_1.find('div', class_='chanquan').stripped_strings))
        col_2 = info.find('div', class_='col-2')
        kanguo = ' '.join(list(col_2.find('div', class_='square').stripped_strings))
        col_3 = info.find('div', class_='col-3')
        price = ' '.join(list(col_3.find('div', class_='price').stripped_strings))
        price_update = str(col_3.find('div', class_='price-pre').string)
        datum = {'city': city,
                 'title': title,
                 'where': where,
                 'other': other,
                 'chanquan': chanquan,
                 'kanguo': kanguo,
                 'price': price,
                 'price': price_update
                 }
        data.append(datum)
    return data

@app.route(r'http://' + city_code + r'\.lianjia\.com/xiaoqu/(pg[0-9]*/)?', js_source=js_source)
async def xiaoqu(url, soup):
    data = []
    #try:
    #    city = cityName.search(str(soup)).group()
    #except:
    #    city = city_name.search(str(soup)).group()
    xiaoqu_list = soup.find('ul', class_='listContent').find_all('li')
    for xiaoqu in xiaoqu_list:
        info = xiaoqu.find('div', class_='info')
        if not info:
            continue
        title = str(info.find('div', class_='title').a.string)
        house_info = ' '.join(list(info.find('div', class_='houseInfo').stripped_strings))
        position_info = ' '.join(list(info.find('div', class_='positionInfo').stripped_strings))
        tags = list(info.find('div', class_='tagList').stripped_strings)
        item_right = xiaoqu.find('div', class_='xiaoquListItemRight')
        price = ' '.join(list(item_right.find('div', class_='xiaoquListItemPrice').stripped_strings))
        sell_count = ' '.join(list(item_right.find('div', class_='xiaoquListItemSellCount').stripped_strings))
        datum = {'city': city,
                 'title': title,
                 'house-info': house_info,
                 'position-info': position_info,
                 'tags': tags,
                 'price': price,
                 'sell-count': sell_count
                 }
        data.append(datum)
    return data

@app.route(r'http://' + city_code + r'\.lianjia\.com/chengjiao/(pg[0-9]*/)?', js_source=js_source)
async def chengjiao(url, soup):
    data = []
    #try:
    #    city = cityName.search(str(soup)).group()
    #except:
    #    city = city_name.search(str(soup)).group()
    chengjiao_list = soup.find('ul', class_='listContent').find_all('li')
    for chengjiao in chengjiao_list:
        info = chengjiao.find('div', class_='info')
        if not info:
            continue
        title = str(info.find('div', class_='title').a.string)
        address = ' '.join(list(info.find('div', class_='address').stripped_strings))
        flood = ' '.join(list(info.find('div', class_='flood').stripped_strings))
        datum = {'city': city,
                 'title': title,
                 'address': address,
                 'flood': flood
                 }
        deal_house_info_bs = info.find('div', class_='dealHouseInfo')
        if deal_house_info_bs:
            deal_house_info = ' '.join(list(deal_house_info_bs.stripped_strings))
            datum['deal_house_info'] = deal_house_info
        data.append(datum)
    return data

@app.route(r'http://' + city_code + r'\.lianjia\.com/')
async def follow(url, soup):
    return None

app.crawl()
