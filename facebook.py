import webapp2
import oauth
import os
from django.utils import simplejson as json

from webutil import web_get,web_post,encode,to_querystring,to_dictionary,read_config

class Facebook(oauth.OAuthHandler):

    def login(self):
        url = self.config['authenticate_url']
        client_id = self.config['consumer_key']
        redirect_uri = self.uri_for("facebook_actions", action="auth_handler", _full=True)

        self.redirect(url.format(client_id,redirect_uri))

    def auth_handler(self):
        if (self.request.params["code"]):
            code = self.request.params["code"]
            url = self.config['request_token_url']
            redirect_uri = self.uri_for("facebook_actions", action="auth_handler", _full=True)
            get_url = url.format(self.config['consumer_key'], redirect_uri, self.config["consumer_secret"], code)
            result = web_get(get_url)

            if (result.status_code == 200):
                token = to_dictionary(result.content)
                self.redirect("{0}?oauth_token={1}".format(self.config['login_callback'],token['access_token']))
            else:
                error = json.loads(result.content)['error']
                for key,value in error.iteritems():
                    self.response.write('{0} : {1} <br />'.format(key,value))
        else:
            self.response.write("error")
            for key,value in self.response.params.iteritems():
                self.response.write("{0}={1} <br /> ".format(key,value))
    
    def get(self, action=None):
        path = os.path.join(os.path.split(__file__)[0], 'config/facebook.json')
        self.config = read_config(path)
        self.config['login_callback'] = self.uri_for("facebook_actions", action="success", _full=True)

        super(Facebook, self).get(action)
