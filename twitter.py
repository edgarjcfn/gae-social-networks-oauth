import webapp2
import urllib
from google.appengine.api.urlfetch import fetch as webfetch, GET, POST

REQUEST_TOKEN_URL = 'http://www.twitter.com/oauth/request_token'

def web_get(url, params=None):
    if params is not None:
        params_str = ""
        for key,value in params.items():
            params_str += "{0}={1}".format(key, value)
        url = "{0}?{1}".format(url, params_str)

    return webfetch(url, None, GET)

def web_post(url, params=None):
    params = urllib.urlencode(params)
    return webfetch(url=url, payload=params, method=POST)

class Twitter(webapp2.RequestHandler):

    def get(self, action=None):

        for key,value in self.request.params.items():
            self.response.write("{0}={1}".format(key,value))
