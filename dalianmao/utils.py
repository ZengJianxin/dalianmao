def cookiestring2dict(cookiestring):
    cookies = dict()
    for item in cookiestring.split(';'):
        terms = item.split('=')
        key, value = terms[0].strip(), '='.join(terms[1:])
        cookies[key] = value
    return cookies
