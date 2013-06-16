import webapp2

from home import Home
from facebook import Facebook
from twitter import Twitter

application = webapp2.WSGIApplication([
    webapp2.Route('/auth/twitter<:/?>', handler=Twitter, name='twitter'),
	webapp2.Route(r'/auth/twitter/<action>', handler=Twitter, name='twitter_actions'),
    webapp2.Route('/auth/facebook<:/?>', handler=Facebook, name='facebook'),
    webapp2.Route(r'/auth/facebook/<action>', handler=Facebook, name='facebook_actions'),
    webapp2.Route(r'/', handler=Home, name='home'),
], debug=True) 
