def cookiestring2dict(cookiestring):
    cookies = dict()
    for item in cookiestring.split(';'):
        key, value = item.split('=')
        cookies[key] = value
    return cookies
