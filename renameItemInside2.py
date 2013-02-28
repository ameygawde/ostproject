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


class renameItemInside2(webapp.RequestHandler): 
  def post(self):
      url = self.request.get('url')
      url_linktext = self.request.get('url_linktext')
      loggedInUser = self.request.get('loggedInUser')
      categorySelected = self.request.get('categ')
      item = self.request.get('item')
      newItem = self.request.get('newItem')
      if newItem == None or newItem == "":
         template_values = {
             'newItemEmpty' : "Yes",
             'loggedInUser' : loggedInUser,
             'categorySelected':categorySelected,
             'url' : url,
             'item':item,
             'url_linktext': url_linktext
         }
         path = os.path.join(os.path.dirname(__file__),'webpages/renameItem2.html')
         self.response.out.write(template.render(path, template_values))
      else:
          items = db.GqlQuery("SELECT * FROM Items WHERE category = :1 AND owner = :2", categorySelected, loggedInUser)
          votes = db.GqlQuery("SELECT * FROM Votes WHERE category = :1 AND owner = :2", categorySelected, loggedInUser)

          for item1 in items:
              if item1.item == item:
                  item1.item = newItem
                  item1.put()

          for vote in votes:
              if vote.winner == item:
                  vote.winner = newItem
                  vote.put()
              if vote.loser == item:
                  vote.loser = newItem
                  vote.put()

          template_values = {
             'renameItemDone' : "Yes",
             'loggedInUser' : loggedInUser,
             'categorySelected':categorySelected,
             'newItem':newItem,
             'item':item,
             'url' : url,
             'url_linktext': url_linktext
          }
          path = os.path.join(os.path.dirname(__file__),'webpages/editCategories.html')
          self.response.out.write(template.render(path, template_values))



