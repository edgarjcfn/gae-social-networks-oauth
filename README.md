Social Network Oauth Connectors for Google App Engine
=====================================================


The aim of this project is to provide an easy way to enable the Oauth
dance in a Google Cloud App.

Support
-------
Currently the supported connectors are facebook and twitter

Tutorial
---------
To use this project:
1 - Setup a Google App Engine Application in Python
2 - Input Secret and Key data into config/facebook_example.json and
config/twitter_example.json
3 - Rename these files to facebook.json and twitter.json respectively
4 - Accessing http://localhost/auth/facebook/login or
http://localhost/auth/twitter/login should start the OAuth dance for
both connectors
5 - Upon success user will be redirected to a default url such as
http://localhost/auth/facebook/success?oauth_token=<TOKEN> 

TODO
====
Add unit tests
Add other social networks
