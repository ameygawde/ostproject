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


class renameCategory(webapp.RequestHandler): 
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
                'renameCategory':"Yes",
                'userCategories':userCategories,
                'loggedInUser' :loggedInUser,
                'url_linktext': url_linktext
          }

          path = os.path.join(os.path.dirname(__file__), 'webpages/userCategories.html')
          self.response.out.write(template.render(path, template_values))
          
      else:
          template_values = {
            'url': url,
            'categorySelected':categorySelected,
            'loggedInUser' :loggedInUser,
            'url_linktext': url_linktext
          }

          path = os.path.join(os.path.dirname(__file__), 'webpages/renameCategory.html')
          self.response.out.write(template.render(path, template_values))
