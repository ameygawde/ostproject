import cgi
import os
import random
import string

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

from Datastores import *


class resultsPage(webapp.RequestHandler): 
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
            'option4Selected':"Yes",
            'url':url,
            'url_linktext':url_linktext
          }
          path = os.path.join(os.path.dirname(__file__), 'webpages/AllCategories.html')
          self.response.out.write(template.render(path, template_values))
      else:
          categorySelected = categoryAndOwner.split('|')[0]
          owner = categoryAndOwner.split('|')[1]
          items = db.GqlQuery("SELECT * FROM Items WHERE category = :1 AND owner = :2", categorySelected, owner)
          votes = db.GqlQuery("SELECT * FROM Votes WHERE category = :1 AND owner = :2", categorySelected, owner)
          itemCount = items.count()
          voteCount = votes.count()
          if itemCount == 0:
              allCategories = db.GqlQuery("SELECT * FROM Categories")
              template_values = {
                'allCategories': allCategories,
                'loggedInUser': loggedInUser,
                'noItemsPresent': "Yes",
                'option4Selected':"Yes",
                'categorySelected': categorySelected,
                'owner': owner,
                'url':url,
                'url_linktext':url_linktext
              }
              path = os.path.join(os.path.dirname(__file__), 'webpages/AllCategories.html')
              self.response.out.write(template.render(path, template_values))
          elif voteCount == 0:
              allCategories = db.GqlQuery("SELECT * FROM Categories")
              template_values = {
                'allCategories': allCategories,
                'loggedInUser': loggedInUser,
                'noVotesPresent': "Yes",
                'option4Selected':"Yes",
                'categorySelected': categorySelected,
                'owner': owner,
                'url':url,
                'url_linktext':url_linktext
              }
              path = os.path.join(os.path.dirname(__file__), 'webpages/AllCategories.html')
              self.response.out.write(template.render(path, template_values))
          else:    
            results = Results.all()
            for r in results:
                r.delete() 
            for item1 in items:
                currentItem = item1.item   
                winCount = 0
                lossCount = 0
                winPercent = 0
                for vote in votes:
                    winner = vote.winner
                    loser = vote.loser
                    if currentItem == winner:
                       winCount+= 1
                    if currentItem == loser:
                       lossCount+= 1
                      
                if winCount == 0 and lossCount == 0:
                    winPercent = 0
                else:
                    sum = winCount + lossCount
                    div = float(winCount)/sum
                    winPercent = div * 100
                    
                result = Results()
                result.category = categorySelected
                result.owner = owner
                result.item = currentItem
                result.winCount = winCount
                result.lossCount = lossCount
                result.winPercent = int(winPercent)
                result.put()
           
            allResults = db.GqlQuery("SELECT * FROM Results WHERE category = :1 AND owner = :2 ORDER BY winPercent DESC ", categorySelected, owner)
          
            template_values = {
              'loggedInUser': loggedInUser,                 
              'allResults': allResults,
              'categorySelected': categorySelected,
              'owner': owner,
              'url':url,
              'url_linktext':url_linktext
            }

            path = os.path.join(os.path.dirname(__file__), 'webpages/resultsPage.html')
            self.response.out.write(template.render(path, template_values))
