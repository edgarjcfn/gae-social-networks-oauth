import webapp2

from home import Home
from facebook import Facebook
from twitter import Twitter

application = webapp2.WSGIApplication([
	webapp2.Route(r'/', handler=Home, name='home'),
	webapp2.Route(r'/auth/facebook', handler=Facebook, name='facebook'),
	webapp2.Route(r'/auth/twitter', handler=Twitter, name='twitter'),
], debug=True) 
