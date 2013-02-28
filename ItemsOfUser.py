import cgi
import os
import random

from xml.dom.minidom import Document
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from Datastores import *

class ItemsOfUser(webapp.RequestHandler):  # Add items to the category
  def post(self):
      categorySelected = self.request.get('categ')
      loggedInUser = self.request.get('loggedInUser')
      url = self.request.get('url')
      url_linktext = self.request.get('url_linktext')
      if categorySelected == None or categorySelected == "":
          userCategories = db.GqlQuery("SELECT * FROM Categories where owner = :1", loggedInUser)
          template_values = {
                'url': url,
                'noOptionSelected':"Yes",
                'userCategories':userCategories,
                'loggedInUser' :loggedInUser,
                'url_linktext': url_linktext
          }

          path = os.path.join(os.path.dirname(__file__), 'webpages/userCategories.html')
          self.response.out.write(template.render(path, template_values))
      else:  
          userItems = db.GqlQuery("SELECT * FROM Items WHERE category = :1 AND owner = :2", categorySelected, loggedInUser)
          self.response.headers['Content-Type'] = 'text/html'
          item=userItems.get()
          if item != None:
              template_values = {
                'userItems': userItems,
                'categorySelected': categorySelected,
                'url':url,
                'url_linktext':url_linktext,
                'loggedInUser': loggedInUser
              }

              path = os.path.join(os.path.dirname(__file__), 'webpages/userItemsPage.html')
              self.response.out.write(template.render(path, template_values))
          else:
              template_values = {
                'userItems': "",
                'categorySelected': categorySelected,
                'url':url,
                'url_linktext':url_linktext,
                'loggedInUser': loggedInUser
              }

              path = os.path.join(os.path.dirname(__file__), 'webpages/userItemsPage.html')
              self.response.out.write(template.render(path, template_values)) 
