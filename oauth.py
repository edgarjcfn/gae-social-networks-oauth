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


def build_signature_string(header_data, post_data, url):
    """ Builds the string that will be hashed in order to sign the request """
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
    """ Applies a hash to the request data in order to sign the request """
    return hmac(encode(consumer_secret)+"&", signature_string, sha1).digest().encode('base64')[:-1]


def get_header_data(config):
    """ Gets the data that will be appended to the signature hash """
    header_data = {
            "oauth_consumer_key" : config['consumer_key'],
            "oauth_nonce" : getrandbits(64),
            "oauth_signature_method" : "HMAC-SHA1",
            "oauth_timestamp" : int(time()),
            "oauth_version" : "1.0"
        }
    return header_data


def build_header_string(header_data):
    """ Builds the Authorization header for the oauth requests """
    header_string = "OAuth "
    encoded_values = []
    for key,value in sorted(header_data.items()):
        encoded_values.append('{0}="{1}"'.format(encode(key), encode(value)))
    header_string += ", ".join(encoded_values)
    return header_string


def create_authorization_header(post_data, header_data, extra_data, config):
    """ Builds the Authorization header, including signature """
    signature_string = build_signature_string(header_data, post_data, config['request_token_url'])
    signature = sign_request(signature_string, config['consumer_secret'])
    header_data["oauth_signature"] = signature
    for key,value in extra_data.iteritems():
        header_data[key] = value
    return build_header_string(header_data)


# ===========
# Web Handler
# ===========
class OAuthHandler(webapp2.RequestHandler):

    def login(self):
            # Build the request
            post_data = {
                "oauth_callback" : self.config['login_callback']
            }

            headers = {
                "Authorization" : create_authorization_header(post_data, get_header_data(self.config), post_data, self.config)   
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