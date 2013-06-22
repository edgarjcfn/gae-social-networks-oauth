import webapp2
import oauth
import os

from webutil import read_config

class Twitter(oauth.OAuthHandler):

    def get(self, action=None):
        path = os.path.join(os.path.split(__file__)[0], 'config/twitter.json')
        self.config = read_config(path)
        self.config['login_callback'] = self.uri_for("twitter_actions", action="success", _full=True)

        super(Twitter, self).get(action)

    