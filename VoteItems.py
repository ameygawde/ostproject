import cgi
import os
import random

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from datetime import *

from Datastores import *


class VoteItems(webapp.RequestHandler): 
  def post(self):
      url = self.request.get('url')
      url_linktext = self.request.get('url_linktext')
      loggedInUser = self.request.get('loggedInUser')
      categoryAndOwner = self.request.get('categ')
      if categoryAndOwner == None or categoryAndOwner == "":
          allCategories = db.GqlQuery("SELECT * FROM Categories")
          template_values = {
            'allCategories': allCategories,
            'loggedInUser': loggedInUser,
            'noOptionSelected': "Yes",
            'url':url,
            'url_linktext':url_linktext
          }
          path = os.path.join(os.path.dirname(__file__), 'webpages/AllCategories.html')
          self.response.out.write(template.render(path, template_values))
      else:    
          categorySelected = categoryAndOwner.split('|')[0]
          owner = categoryAndOwner.split('|')[1]
          
          result = db.GqlQuery("SELECT * FROM Categories where owner = :1 AND category = :2", owner,categorySelected)
          for r in result:
            expDate = r.expDate
          today = date.today()
          inTime=""
          if expDate == None or expDate == "":
             inTime ="Yes"
          else:   
              if expDate < today:
                 timeOut = "Yes"
              else:
                  inTime="Yes" 
                 
          totalItems = db.GqlQuery("SELECT * FROM Items WHERE category = :1 AND owner = :2", categorySelected, owner)
          itemCount = totalItems.count()
          less_Items = ""
          if itemCount < 2:
            less_Items = "Yes"
          elif itemCount == 2:
            i = 0
            j = 1
          else:        
            i = random.randint(0, itemCount-1)
            j = random.randint(0, itemCount-1)
            while i == j:
              i = random.randint(0, itemCount-1)
              j = random.randint(0, itemCount-1)

          if less_Items == "Yes":
            allCategories = db.GqlQuery("SELECT * FROM Categories")
            template_values = {
              'allCategories': allCategories,
              'loggedInUser': loggedInUser,
              'categorySelected': categorySelected,
              'less_Items' : less_Items,
              'owner': owner,
              'url':url,
              'url_linktext':url_linktext
            }
            path = os.path.join(os.path.dirname(__file__), 'webpages/AllCategories.html')
            self.response.out.write(template.render(path, template_values))
          else:  
              counter = 0
       
              item1 = ""
              item2 = ""    
              for item in totalItems:
                  if counter == i:
                      item1 = item.item
                  if counter == j:
                      item2 = item.item
                  counter+= 1
              if inTime != "Yes":
                  allCategories = db.GqlQuery("SELECT * FROM Categories")
                  template_values = {
                    'allCategories': allCategories,
                    'loggedInUser': loggedInUser,
                    'categorySelected': categorySelected,
                    'timeOut' : timeOut,
                    'expDate':expDate,
                    'owner': owner,
                    'url':url,
                    'url_linktext':url_linktext
                  }
                  path = os.path.join(os.path.dirname(__file__), 'webpages/AllCategories.html')
                  self.response.out.write(template.render(path, template_values))
              else:  
                  template_values = {
                    'item1': item1,
                    'item2': item2,
                    'loggedInUser': loggedInUser,
                    'categorySelected': categorySelected,
                    'owner': owner,
                    'url' : url,
                    'url_linktext': url_linktext
                  }

                  path = os.path.join(os.path.dirname(__file__), 'webpages/VotePage.html')
                  self.response.out.write(template.render(path, template_values))
