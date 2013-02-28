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


class deleteItemInside(webapp.RequestHandler): 
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
          path = os.path.join(os.path.dirname(__file__), 'webpages/deleteItem.html')
          self.response.out.write(template.render(path, template_values))
      else:
          items = db.GqlQuery("SELECT * FROM Items WHERE category = :1 AND owner = :2", categorySelected, loggedInUser)
          votes = db.GqlQuery("SELECT * FROM Votes WHERE category = :1 AND owner = :2", categorySelected, loggedInUser)

          for item1 in items:
              if item1.item == item:
                  item1.delete()

          for vote in votes:
              if vote.winner == item:
                  vote.delete()
              if vote.loser == item:
                  vote.delete()

          userItems = db.GqlQuery("SELECT * FROM Items WHERE category = :1 AND owner = :2", categorySelected, loggedInUser)
          count=userItems.count()
          if count == 0:
              template_values = {
                'url': url,
                'noItems':"Yes",
                'deleteItemDone' : "Yes",
                'item':item,
                'categorySelected':categorySelected,
                'loggedInUser' :loggedInUser,
                'url_linktext': url_linktext
              }

              path = os.path.join(os.path.dirname(__file__), 'webpages/editCategories.html')
              self.response.out.write(template.render(path, template_values))
              
          else:    
              template_values = {
                 'deleteItemDone' : "Yes",
                 'loggedInUser' : loggedInUser,
                 'categorySelected':categorySelected,
                 'userItems':userItems,
                 'item':item,
                 'url' : url,
                 'url_linktext': url_linktext
              }
              path = os.path.join(os.path.dirname(__file__),'webpages/editCategories.html')
              self.response.out.write(template.render(path, template_values))

                  
          
