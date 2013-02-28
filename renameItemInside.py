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


class renameItemInside(webapp.RequestHandler): 
  def post(self):
      url = self.request.get('url')
      url_linktext = self.request.get('url_linktext')
      loggedInUser = self.request.get('loggedInUser')
      categorySelected = self.request.get('categorySelected')
      item = self.request.get('itemName')
      if item == None or item == "":
          userItems = db.GqlQuery("SELECT * FROM Items WHERE category = :1 AND owner = :2", categorySelected, loggedInUser)
          template_values = {
            'url': url,
            'noOptionSelected':"Yes",
            'userItems':userItems,
            'categorySelected':categorySelected,
            'loggedInUser' :loggedInUser,
            'url_linktext': url_linktext
          }
          path = os.path.join(os.path.dirname(__file__), 'webpages/renameItem.html')
          self.response.out.write(template.render(path, template_values))
      else:
          template_values = {
             'loggedInUser' : loggedInUser,
             'categorySelected':categorySelected,
             'item':item,
             'url' : url,
             'url_linktext': url_linktext
          }
          path = os.path.join(os.path.dirname(__file__),'webpages/renameItem2.html')
          self.response.out.write(template.render(path, template_values))

                  
          

