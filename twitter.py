import webapp2
import oauth

class Twitter(oauth.OAuthHandler):

    def get(self, action=None):
        self.config = {
            'authenticate_url' : 'https://api.twitter.com/oauth/authenticate',
            'request_token_url' : 'https://api.twitter.com/oauth/request_token',
            'consumer_secret' : "VCOp4U4kKtd1EovxksktiPnfaYpSPhogpQTshHDYn4",
            'consumer_key' : "wxLnvuFqFfrqaYfVx3RKdg",
            'login_callback' : self.uri_for("twitter_actions", action="obtain_access_token", _full=True)
        }

        super(Twitter, self).get(action)

    