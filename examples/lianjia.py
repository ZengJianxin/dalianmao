import re

from dalianmao import DaLianMao, Options

cityName = re.compile(r"(?<=cityName: ').*(?=')")
city_name = re.compile(r"(?<=city_name: ').*(?=')")
total_page = re.compile('\"totalPage\":[0-9]*')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    #'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
    }
    

options = Options(name='lianjia',
                  start_urls= ['http://xm.lianjia.com/', ],
                  headers=HEADERS,
                  dynamic=True,
                  concurrence=3,
                  magic=5
                 )
app = DaLianMao(options)

@app.route(r'http://xm\.fang\.lianjia\.com/loupan/(pg[0-9]*/)?')
async def loupan(url, soup):
    data = []
    try:
        city = cityName.search(str(soup)).group()
    except:
        city = city_name.search(str(soup)).group()
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
        other = list(col_1.find('div', class_='other').stripped_strings)
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

@app.route(r'http://xm\.lianjia\.com/ershoufang/(pg[0-9]*/)?')
async def ershoufang(url, soup):
    data = []
    try:
        city = cityName.search(str(soup)).group()
    except:
        city = city_name.search(str(soup)).group()
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

@app.route(r'http://xm\.lianjia\.com/zufang/(pg[0-9]*/)?')
async def zufang(url, soup):
    data = []
    try:
        city = cityName.search(str(soup)).group()
    except:
        city = city_name.search(str(soup)).group()
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

@app.route(r'http://xm\.lianjia\.com/xiaoqu/(pg[0-9]*/)?')
async def xiaoqu(url, soup):
    data = []
    try:
        city = cityName.search(str(soup)).group()
    except:
        city = city_name.search(str(soup)).group()
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

@app.route(r'http://xm\.lianjia\.com/chengjiao/(pg[0-9]*/)?')
async def chengjiao(url, soup):
    data = []
    try:
        city = cityName.search(str(soup)).group()
    except:
        city = city_name.search(str(soup)).group()
    chengjiao_list = soup.find('ul', class_='listContent').find_all('li')
    for chengjiao in chengjiao_list:
        info = chengjiao.find('div', class_='info')
        if not info:
            continue
        title = str(info.find('div', class_='title').a.string)
        address = ' '.join(list(info.find('div', class_='address').stripped_strings))
        flood = ' '.join(list(info.find('div', class_='flood').stripped_strings))
        deal_house_info_bs = info.find('div', class_='dealHouseInfo')
        if deal_house_info:
            deal_house_info = ' '.join(list(deal_house_info_bs.stripped_strings))
        datum = {'city': city,
                 'title': title,
                 'address': address,
                 'flood': flood,
                 'house_info': deal_house_info
                 }
        data.append(datum)
    return data

@app.route(r'http://xm\.lianjia\.com/')
async def follow(url, soup):
    return None

app.crawl()
