import urllib
import cgi

from urllib import urlencode, quote as urlquote
from google.appengine.api.urlfetch import fetch as urlfetch, GET, POST


def web_get(url, params=None):
    """ Returns the contents of (url), by accessing it through GET """
    if params is not None:
        params_str = ""
        for key,value in params.items():
            params_str += "{0}={1}".format(key, value)
        url = "{0}?{1}".format(url, params_str)
    return urlfetch(url, None, GET)


def web_post(url, params=None, headers={}):
    """ Returns the contents of (url), by accessing it through POST """
    params = urllib.urlencode(params)
    return urlfetch(url=url, payload=params, method=POST, headers=headers, validate_certificate=False)


def encode(text):
    """ URL-encodes text """
    return urlquote(str(text), '')


def to_querystring(params):
    """ Joins the given (params) in querystring format """
    return '&'.join(
        '{0}={1}'.format(encode(i), encode(params[i])) for i in sorted(params)
        )

