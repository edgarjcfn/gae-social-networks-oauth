import webapp2
import urllib
from hashlib import sha1
from hmac import new as hmac
from random import getrandbits
from time import time
from urllib import urlencode, quote as urlquote

from google.appengine.api.urlfetch import fetch as webfetch, GET, POST

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
# REQUEST_TOKEN_URL = 'http://localhost:8080/auth/twitter'

# CONSUMER_SECRET = "VCOp4U4kKtd1EovxksktiPnfaYpSPhogpQTshHDYn4"
CONSUMER_SECRET = "MCD8BKwGdgPHvAuvgvz4EQpqDAtx89grbuNMRd7Eh98"

CONSUMER_KEY = "wxLnvuFqFfrqaYfVx3RKdg"

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
    return webfetch(url=url, payload=params, method=POST, headers=headers, validate_certificate=False)


def _is(action, expected):
    return action.lower() == expected

def encode(text):
    return urlquote(str(text), '')

def to_querystring(params):
    return '&'.join(
        '{0}={1}'.format(encode(i), encode(params[i])) for i in sorted(params)
        )

def build_signature_string(header_data, post_data, url):
    all_data = {}

    for key, value in header_data.items():
        all_data[key] = value
    for key, value in post_data.items():
        all_data[key] = value

    encoded_data = to_querystring(all_data)

    message = '&'.join(map(encode, [
            "POST", url, encoded_data
            ]))

    return message

def sign_request(signature_string):
    return hmac(encode(CONSUMER_SECRET)+"&", signature_string, sha1).digest().encode('base64')[:-1]

def build_header_string(header_data):
    header_string = "OAuth "
    encoded_values = []
    for key,value in header_data.items():
        encoded_values.append('{0}="{1}"'.format(encode(key), encode(value)))

    header_string += ", ".join(encoded_values)
    return header_string

# ===========
# Web Handler
# ===========
class Twitter(webapp2.RequestHandler):

    def get(self, action=None):
        if _is(action, "login"): #Get request token
            # Build the request
            callback_url = self.uri_for("twitter_actions", action="req_token_callback", _full=True)
            

            header_data = {
                "oauth_consumer_key" : CONSUMER_KEY,
                "oauth_nonce" : getrandbits(64),
                "oauth_signature_method" : "HMAC-SHA1",
                "oauth_timestamp" : int(time()),
                "oauth_version" : "1.0"
            }

            post_data = {
                "oauth_callback" : callback_url
            }

            signature_string = build_signature_string(header_data, post_data, REQUEST_TOKEN_URL)
            signature = sign_request(signature_string)
            
            header_data["oauth_signature_method"] = signature
            header_data["oauth_callback"] = encode(callback_url)

            header_string = build_header_string(header_data)

            # debug data
            self.response.write("signature_string: %s <br /><br /> " % signature_string)
            self.response.write("signature: %s <br /><br /> " % signature)
            self.response.write("header_string: %s <br /><br /> " % header_string)


            for key,value in post_data.iteritems():
                post_data[key] = encode(value)

            # Post request
            result = web_post(url=REQUEST_TOKEN_URL, params=post_data, headers={"Authorization" : header_string})
            self.response.write("<br />status: {0}<br />message: {1}".format(result.status_code, result.content))

    def post(self, action=None):
        self.response.write("POST lands here <br />")
        self.response.write("Params: <br />")
        for key,value in self.request.params.iteritems():
            self.response.write(key + ":" +value)
            self.response.write("<br />")
        self.response.write("<br />")
        self.response.write("Headers: <br />")
        for key,value in self.request.headers.iteritems():
            self.response.write(key + ":" +value)
            self.response.write("<br />")