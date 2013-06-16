import webapp2
import oauth
from webutil import web_get,web_post,encode,to_querystring

class Facebook(oauth.OAuthHandler):

    def login(self):
        url = 'https://www.facebook.com/dialog/oauth?client_id={0}&redirect_uri={1}'
        client_id = '197666783690495'
        redirect_uri = self.uri_for("facebook_actions", action="auth_handler", _full=True)

        self.redirect(url.format(client_id,redirect_uri))

    def auth_handler(self):
        self.response.write('eaeaeeee')
    
    def get(self, action=None):
        self.config = {
            'authenticate_url' : 'https://api.twitter.com/oauth/authenticate',
            'request_token_url' : 'https://api.twitter.com/oauth/request_token',
            'consumer_secret' : "fd813c9bac5c49d7e2d02a386176f1a3",
            'consumer_key' : "197666783690495",
            'login_callback' : self.uri_for("twitter_actions", action="obtain_access_token", _full=True)
        }

        super(Facebook, self).get(action)
