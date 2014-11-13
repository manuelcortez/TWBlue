# -*- coding: utf-8 -*-
import BaseHTTPServer
import webbrowser
from twython import Twython, TwythonError
import application
import authorisationHandler

class twitter(object):

 def login(self, user_key, user_secret):
  self.twitter = Twython(application.app_key, application.app_secret, user_key, user_secret)
  self.credentials = self.twitter.verify_credentials()

 def authorise(self, settings):
  httpd = BaseHTTPServer.HTTPServer(('127.0.0.1', 8080), authorisationHandler.handler)
  twitter = Twython(application.app_key, application.app_secret)
  auth = twitter.get_authentication_tokens("http://127.0.0.1:8080")
  webbrowser.open_new_tab(auth['auth_url'])
#  global logged, verifier
  while authorisationHandler.logged == False:
   httpd.handle_request()
  self.twitter = Twython(application.app_key, application.app_secret, auth['oauth_token'], auth['oauth_token_secret'])
  final = self.twitter.get_authorized_tokens(authorisationHandler.verifier)
  self.save_configuration(settings, final["oauth_token"], final["oauth_token_secret"])

 def save_configuration(self, settings, user_key, user_secret):
  settings["twitter"]["user_key"] = user_key
  settings["twitter"]["user_secret"] = user_secret
  settings.write()
