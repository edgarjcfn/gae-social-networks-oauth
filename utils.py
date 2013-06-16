from google.appengine.api.urlfetch import fetch as urlfetch, GET, POST

def web_get(url, params=None):
    if params is not None:
        params_str = ""
        for key,value in params.items():
            params_str += "{0}={1}".format(key, value)
        url = "{0}?{1}".format(url, params_str)

    return urlfetch(url, None, GET)

def web_post(url, params=None, headers={}):
    params = urllib.urlencode(params)
    return urlfetch(url=url, payload=params, method=POST, headers=headers, validate_certificate=False)

def encode(text):
    return urlquote(str(text), '')

def to_querystring(params):
    return '&'.join(
        '{0}={1}'.format(encode(i), encode(params[i])) for i in sorted(params)
        )