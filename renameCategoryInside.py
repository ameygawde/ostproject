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


class renameCategoryInside(webapp.RequestHandler): 
  def post(self):
      url = self.request.get('url')
      url_linktext = self.request.get('url_linktext')
      loggedInUser = self.request.get('loggedInUser')
      categorySelected = self.request.get('categ')
      newCategory = self.request.get('newCategory')
      if newCategory == None or newCategory == "":
         template_values = {
             'newcategoryEmpty' : "Yes",
             'loggedInUser' : loggedInUser,
             'categorySelected':categorySelected,
             'url' : url,
             'url_linktext': url_linktext
         }
         path = os.path.join(os.path.dirname(__file__),'webpages/renameCategory.html')
         self.response.out.write(template.render(path, template_values))
      else:
          results1 = db.GqlQuery("SELECT * FROM Categories WHERE category = :1 AND owner = :2", categorySelected, loggedInUser)
          for r1 in results1:
             r1.category = newCategory
             r1.put()
             
          results2 = db.GqlQuery("SELECT * FROM Items WHERE category = :1 AND owner = :2", categorySelected, loggedInUser)
          for r2 in results2:
             r2.category = newCategory
             r2.put()

          template_values = {
             'renameDone' : "Yes",
             'loggedInUser' : loggedInUser,
             'categorySelected':categorySelected,
             'newName':newCategory,
             'url' : url,
             'url_linktext': url_linktext
          }
          path = os.path.join(os.path.dirname(__file__),'webpages/editCategories.html')
          self.response.out.write(template.render(path, template_values))
