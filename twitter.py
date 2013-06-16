import webapp2
import urllib

from hashlib import sha1
from hmac import new as hmac
from random import getrandbits
from time import time
from urllib import urlencode, quote as urlquote
import cgi
from google.appengine.api.urlfetch import fetch as urlfetch, GET, POST

# ==================
# Helper Methods
# ==================
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

def sign_request(signature_string, consumer_secret):
    return hmac(encode(consumer_secret)+"&", signature_string, sha1).digest().encode('base64')[:-1]

def build_header_string(header_data):
    header_string = "OAuth "
    encoded_values = []
    for key,value in sorted(header_data.items()):
        encoded_values.append('{0}="{1}"'.format(encode(key), encode(value)))

    header_string += ", ".join(encoded_values)
    return header_string

def create_authorization_header(post_data, extra_data, config):
            header_data = {
                "oauth_consumer_key" : config['consumer_key'],
                "oauth_nonce" : getrandbits(64),
                "oauth_signature_method" : "HMAC-SHA1",
                "oauth_timestamp" : int(time()),
                "oauth_version" : "1.0"
            }

            signature_string = build_signature_string(header_data, post_data, config['request_token_url'])
            signature = sign_request(signature_string, config['consumer_secret'])
            
            header_data["oauth_signature"] = signature
            
            for key,value in extra_data.iteritems():
                header_data[key] = value

            return build_header_string(header_data)

# ===========
# Web Handler
# ===========
class Twitter(webapp2.RequestHandler):

    config = {
        'authenticate_url' : 'https://api.twitter.com/oauth/authenticate',
        'request_token_url' : 'https://api.twitter.com/oauth/request_token',
        'consumer_secret' : "VCOp4U4kKtd1EovxksktiPnfaYpSPhogpQTshHDYn4",
        'consumer_key' : "wxLnvuFqFfrqaYfVx3RKdg"
    }

    def login(self):
            # Build the request
            callback_url = self.uri_for("twitter_actions", action="obtain_access_token", _full=True)
            
            post_data = {
                "oauth_callback" : callback_url
            }

            headers = {
                "Authorization" : create_authorization_header(post_data, post_data, self.config)   
            }

            # Post request
            result = web_post(url=self.config['request_token_url'], params={}, headers=headers)
            if (result.status_code == 200):
                result_params = cgi.parse_qs(result.content)
                self.redirect("{0}?{1}={2}".format(self.config['authenticate_url'], "oauth_token", result_params["oauth_token"][0]))

    def obtain_access_token(self):
        for key,value in self.request.params.iteritems():
            self.response.write("{0} = {1} <br />".format(key,value))


    def get(self, action=None):
        if action != "" and action != "/":
            try:
                function = getattr(self, action)
                function()
            except AttributeError:
                self.response.write("method {0} was not found".format(action))


    def post(self, action=None):
        self.response.write("<br /> ======================= <br />")
        self.response.write("POST lands here <br />")
        self.response.write("======================= <br />")
        self.response.write("Params: <br />")
        for key,value in self.request.params.iteritems():
            self.response.write(key + "=" +value)
            self.response.write("<br />")
        self.response.write("<br />")
        self.response.write("Headers: <br />")
        for key,value in self.request.headers.iteritems():
            self.response.write(key + ":" +value)
            self.response.write("<br />")