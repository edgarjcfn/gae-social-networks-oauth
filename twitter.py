import webapp2
import urllib
from hashlib import sha1
from hmac import new as hmac
from random import getrandbits
from time import time
from urllib import urlencode, quote as urlquote

from google.appengine.api.urlfetch import fetch as webfetch, GET, POST

REQUEST_TOKEN_URL = 'http://www.twitter.com/oauth/request_token'
APP_SECRET = "VCOp4U4kKtd1EovxksktiPnfaYpSPhogpQTshHDYn4"

# ==============
# Helper methods
# ==============
def web_get(url, params=None):
    if params is not None:
        params_str = ""
        for key,value in params.items():
            params_str += "{0}={1}".format(key, value)
        url = "{0}?{1}".format(url, params_str)

    return webfetch(url, None, GET)

def web_post(url, params=None, headers={}):
    params = urllib.urlencode(params)
    return webfetch(url=url, payload=params, method=POST, headers=headers)


def _is(action, expected):
    return action.lower() == expected

def encode(text):
    return urlquote(str(text), '')

def sign_request(header_data, post_data, url):
    all_data = {}

    for key, value in header_data.items():
        all_data[key] = value
    for key, value in post_data.items():
        all_data[key] = value

    message = '&'.join(map(encode, [
            "POST", url, '&'.join(
                '%s=%s' % (encode(i), encode(all_data[i])) for i in sorted(all_data)
                )
            ]))

    return hmac(APP_SECRET, message, sha1).digest().encode('base64')[:-1]

# ===========
# Web Handler
# ===========
class Twitter(webapp2.RequestHandler):

    def get(self, action=None):
        if _is(action, "login"): #Get request token
            # Build the request
            callback_url = self.uri_for("twitter_actions", action="req_token_callback", _full=True)

            header_data = {
                "oauth_consumer_key" : "",
                "oauth_nonce" : getrandbits(64),
                "oauth_signature_method" : "HMAC-SHA1",
                "oauth_timestamp" : int(time()),
                "oauth_version" : "1.0"
            }

            post_data = {
                "oauth_callback" : callback_url
            }

            msg = sign_request(header_data, post_data, REQUEST_TOKEN_URL)
            # self.response.write(msg)

            header_data["oauth_signature"] = sign_request(header_data, post_data, REQUEST_TOKEN_URL)

            # Post request
            result = web_post(REQUEST_TOKEN_URL, post_data, header_data)
            self.response.write("{0}<br />{1}".format(result.status_code, result.content))