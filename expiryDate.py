import os
import commands
import random

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from xml.dom.minidom import *

from Datastores import *


class expiryDate(webapp.RequestHandler): 
  def post(self):
      url = self.request.get('url')
      url_linktext = self.request.get('url_linktext')
      loggedInUser = self.request.get('loggedInUser')
      categorySelected = self.request.get('categ')
      if categorySelected == None or categorySelected == "":
          userCategories = db.GqlQuery("SELECT * FROM Categories where owner = :1", loggedInUser)
          template_values = {
                'url': url,
                'noOptionSelected':"Yes",
                'expiryDate':"Yes",
                'userCategories':userCategories,
                'loggedInUser' :loggedInUser,
                'url_linktext': url_linktext
          }

          path = os.path.join(os.path.dirname(__file__), 'webpages/userCategories.html')
          self.response.out.write(template.render(path, template_values))
          
      else:
          result = db.GqlQuery("SELECT * FROM Categories where owner = :1 AND category = :2", loggedInUser,categorySelected)
          for r in result:
            expDate = r.expDate
          expiryDate ="No"
          noExpiryDat="No"
          if expDate == None or expDate == "":
              noExpiryDat ="Yes"
          else:
              expiryDate="Yes"

          if expiryDate=="No":
              template_values = {
                'url': url,
                'noExpiryDate':"Yes",
                'categorySelected':categorySelected,
                'loggedInUser' :loggedInUser,
                'url_linktext': url_linktext
              }

              path = os.path.join(os.path.dirname(__file__), 'webpages/expiryDate.html')
              self.response.out.write(template.render(path, template_values))
          else: 
              template_values = {
                'url': url,
                'expAlready':"Yes",
                'expDate':expDate,
                'categorySelected':categorySelected,
                'loggedInUser' :loggedInUser,
                'url_linktext': url_linktext
              }

              path = os.path.join(os.path.dirname(__file__), 'webpages/expiryDate.html')
              self.response.out.write(template.render(path, template_values))
