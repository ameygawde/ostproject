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


class importXML(webapp.RequestHandler): 
  def post(self):
      url = self.request.get('url')
      url_linktext = self.request.get('url_linktext')
      loggedInUser = self.request.get('loggedInUser')
      file1=self.request.get('xmlfile')
      
      if file1 != "":
        contents = self.request.POST.multi['xmlfile'].file
        doc = xml.dom.minidom.parse(contents)
        data = doc.getElementsByTagName("NAME");
        itemList = [];
        for dat in data:
            itemList.append(dat.firstChild.nodeValue);
        category = itemList[0];
        itemList.remove(category);

        userCategories = db.GqlQuery("SELECT * FROM Categories WHERE category = :1 AND owner = :2", category, loggedInUser)
        count=userCategories.count()

        #if count == 0 , insert freshly else update previous

        if count == 0:
           newCategory = Categories()
           newCategory.owner = loggedInUser
           newCategory.category = category
           newCategory.put()

           for item in itemList:
                newItem = Items()
                newItem.category = category
                newItem.owner = loggedInUser
                newItem.item = item
                newItem.put()
        
        else:
            items = db.GqlQuery("SELECT * FROM Items WHERE category = :1 AND owner = :2", category, loggedInUser)
            votes = db.GqlQuery("SELECT * FROM Votes WHERE category = :1 AND owner = :2", category, loggedInUser)

            #to add a new item
            for newItem in itemList:
                itemFound = False
                for item in items:
                    if item.item == newItem:
                         itemFound = True
                         break
                if itemFound == False:
                   newerItem = Items()
                   newerItem.category = category
                   newerItem.owner = loggedInUser
                   newerItem.item = newItem
                   newerItem.put()

            deletedItemsList=[]
            #to remove a old item       
            for item in items:
                itemFound = False
                for newItem in itemList:
                    if newItem == item.item:
                        itemFound = True
                        break
                if itemFound == False:
                   deletedItemsList.append(item.item)
                   item.delete()

            #to remove the deleted item votes
            for deletedItem in deletedItemsList:
                for vote in votes:
                    if vote.winner == deletedItem:
                        vote.delete()
                    if vote.loser == deletedItem:
                        vote.delete()
                      
            template_values = {
              'imported' : "Yes",
              'user': loggedInUser,
              'categorySelected': category,
              'url':url,
              'url_linktext':url_linktext
            }
            path = os.path.join(os.path.dirname(__file__), 'webpages/index1.html')
            self.response.out.write(template.render(path, template_values))
      else:
           template_values = {
              'noFilechosen' : "Yes",
              'loggedInUser': loggedInUser,
              'url':url,
              'url_linktext':url_linktext
           }
           path = os.path.join(os.path.dirname(__file__), 'webpages/importXML.html')
           self.response.out.write(template.render(path, template_values)) 
  
