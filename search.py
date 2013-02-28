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


class search(webapp.RequestHandler): 
  def post(self):
      url = self.request.get('url')
      url_linktext = self.request.get('url_linktext')
      loggedInUser = self.request.get('loggedInUser')
      search = self.request.get('search')
      if search == None or search == "":
         template_values = {
             'searchEmpty' : "Yes",
             'loggedInUser' : loggedInUser,
             'url' : url,
             'url_linktext': url_linktext
         }
         path = os.path.join(os.path.dirname(__file__),'webpages/search.html')
         self.response.out.write(template.render(path, template_values))
      else:
          allCategories = db.GqlQuery("SELECT * FROM Categories")
          allItems = db.GqlQuery("SELECT * FROM Items")

          searchResults=[]
          
          for category in allCategories:
              if category.category.lower() == search.lower():
                  searchResults.append('Category '+ category.category+ ' owned by ' + category.owner)
              if category.owner.lower() == search.lower():
                  searchResults.append('The user: ' + '+category.owner+')

          for category in allCategories:
              if category.category.find(' ') != -1:
                  part1 = category.category.split(' ',1)[0]
                  part2 = category.category.split(' ',1)[1]
                  if part1.lower() == search.lower():
                      searchResults.append('Category '+ category.category+ ' owned by ' + category.owner)
                  if part2.lower() == search.lower():
                      searchResults.append('Category '+ category.category+ ' owned by ' + category.owner)
              if category.owner.find(' ') != -1:
                  part1 = category.owner.split(' ',1)[0]
                  part2 = category.owner.split(' ',1)[1]
                  if part1.lower() == search.lower():
                      searchResults.append('The user: ' + '+category.owner+')
                  if part2.lower() == search.lower():
                      searchResults.append('The user: ' + '+category.owner+')

          for category in allCategories:
              if  search.find(' ') != -1:
                  part1 = search.split(' ',1)[0]
                  part2 = search.split(' ',1)[1]
                  if part1.lower() == category.category.lower():
                      searchResults.append('Category '+ category.category+ ' owned by ' + category.owner)
                  if part2.lower() == category.category.lower():
                      searchResults.append('Category '+ category.category+ ' owned by ' + category.owner)
                  if part1.lower() == category.owner.lower():
                      searchResults.append('The user: ' + '+category.owner+')
                  if part2.lower() == category.owner.lower():
                      searchResults.append('The user: ' + '+category.owner+')

          for item in allItems:
              if item.item.lower() == search.lower():
                  searchResults.append('Item ' + item.item+ ' from category ' + item.category +' owned by ' + item.owner)

          for item in allItems:
              if item.item.find(' ') != -1:
                  part1 = item.item.split(' ',1)[0]
                  part2 = item.item.split(' ',1)[1]
                  if part1.lower() == search.lower():
                      searchResults.append('Item ' + item.item+ ' from category ' + item.category +' owned by ' + item.owner)
                  if part2.lower() == search.lower():
                      searchResults.append('Item ' + item.item+ ' from category ' + item.category +' owned by ' + item.owner)

          for item in allItems:
              if search.find(' ') != -1:
                  part1 = search.split(' ',1)[0]
                  part2 = search.split(' ',1)[1]
                  if part1.lower() == item.item.lower():
                      searchResults.append('Item ' + item.item+ ' from category ' + item.category +' owned by ' + item.owner)
                  if part2.lower() == item.item.lower():
                      searchResults.append('Item ' + item.item+ ' from category ' + item.category +' owned by ' + item.owner)

          count =0
          for s in searchResults:
              count+=1

          if count ==0:
               template_values = {
                 'searchResults' : searchResults,
                 'noResults':"Yes",
                 'search': search,
                 'loggedInUser' : loggedInUser,
                 'url' : url,
                 'url_linktext': url_linktext
               }
               path = os.path.join(os.path.dirname(__file__),'webpages/searchResults.html')
               self.response.out.write(template.render(path, template_values))
          else:
              
              template_values = {
                 'searchResults' : searchResults,
                 'search': search,
                 'loggedInUser' : loggedInUser,
                 'url' : url,
                 'url_linktext': url_linktext
              }
              path = os.path.join(os.path.dirname(__file__),'webpages/searchResults.html')
              self.response.out.write(template.render(path, template_values))    



                  
