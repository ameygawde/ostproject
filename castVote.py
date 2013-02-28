import cgi
import os
import random

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from Datastores import *


class castVote(webapp.RequestHandler): 
  def post(self):
      url = self.request.get('url')
      url_linktext = self.request.get('url_linktext')
      loggedInUser = self.request.get('loggedInUser')
      categorySelected = self.request.get('categorySelected')
      owner = self.request.get('owner')
      selectedItem = self.request.get('selectedItem')
      item1 = self.request.get('item1')
      item2 = self.request.get('item2')
      if selectedItem == None or selectedItem == "":
          totalItems = db.GqlQuery("SELECT * FROM Items WHERE category = :1 AND owner = :2", categorySelected, owner)
          itemCount = totalItems.count()
          if itemCount == 2:
              i = 0
              j = 1
          else:        
              i = random.randint(0, itemCount-1)
              j = random.randint(0, itemCount-1)
              while i == j:
                  i = random.randint(0, itemCount-1)
                  j = random.randint(0, itemCount-1)
      
          counter = 0
          item11 = ""
          item22 = ""    
          for item in totalItems:
              if counter == i:
                 item11 = item.item
              if counter == j:
                 item22 = item.item
              counter+= 1
          template_values = {
             'item1': item11,
             'item2': item22,
             'loggedInUser': loggedInUser,
             'categorySelected': categorySelected,
             'noItemSelected':"Yes",
             'owner': owner,
             'url' : url,
             'url_linktext': url_linktext
          }

          path = os.path.join(os.path.dirname(__file__), 'webpages/VotePage.html')
          self.response.out.write(template.render(path, template_values))
          
      else:
           vote = Votes()
           vote.category = self.request.get('categorySelected')
           vote.owner = self.request.get('owner')
           losingItem=""
           if selectedItem == item1:
              vote.winner = selectedItem
              vote.loser = item2
              losingItem=item2
              vote.put()
           if selectedItem == item2:
              vote.winner = selectedItem
              vote.loser = item1
              losingItem=item1
              vote.put()
              
           totalItems = db.GqlQuery("SELECT * FROM Items WHERE category = :1 AND owner = :2", categorySelected, owner)
           itemCount = totalItems.count()
           if itemCount == 2:
             i = 0
             j = 1
           else:        
              i = random.randint(0, itemCount-1)
              j = random.randint(0, itemCount-1)
              while i == j:
                i = random.randint(0, itemCount-1)
                j = random.randint(0, itemCount-1)
      
           counter = 0
           item11 = ""
           item22 = ""
           
           for item in totalItems:
              if counter == i:
                  item11 = item.item
              if counter == j:
                  item22 = item.item
              counter+= 1    
      
           
           template_values = {
              'voteCasted': "Yes",
              'loggedInUser': loggedInUser,
              'selectedItem': selectedItem,
              'item1': item11,
              'item2': item22,
              'losingItem':losingItem,
              'categorySelected': categorySelected,
              'owner': owner,
              'url' : url,
              'url_linktext': url_linktext
           }

           path = os.path.join(os.path.dirname(__file__), 'webpages/VotePage.html')
           self.response.out.write(template.render(path, template_values))     
