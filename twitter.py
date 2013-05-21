import webapp2
import urllib


REQUEST_TOKEN_URL = 'http://www.twitter.com/oauth/request_token'
class Twitter(webapp2.RequestHandler):

    request_token = None;

    def get(self):
        if not self.has_request_token():
        # Initial state: obtain request token
            self.obtain_request_token()
        else:
        # Has request token
            self.redirect_to_auth_page()

    def has_request_token(self):
        return self.request_token != None

    def obtain_request_token(self):
        request_params = {
            'oauth_callback' : webapp2.uri_for('twitter', _full=True),
        }
        self.redirect("%s?%s" % (REQUEST_TOKEN_URL, urllib.urlencode(request_params)))
    def redirect_to_auth_page(self):
        self.response.write('Redirecting to auth page!')