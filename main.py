import cgi
import datetime
import urllib
import wsgiref.handlers
import os
from google.appengine.ext.webapp import template

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from MainMenu import MainMenu
from ItemsOfUser import ItemsOfUser
from addItem import addItem
from VoteItems import VoteItems
from castVote import castVote
from resultsPage import resultsPage
from exportXML import exportXML
from importXML import importXML
from editCategories import editCategories
from renameCategory import renameCategory
from renameCategoryInside import renameCategoryInside
from deleteCategory import deleteCategory
from deleteCategoryInside import deleteCategoryInside
from renameItem import renameItem
from renameItemInside import renameItemInside
from renameItemInside2 import renameItemInside2
from deleteItem import deleteItem
from deleteItemInside import deleteItemInside
from search import search
from expiryDate import expiryDate
from expiryDateInside import expiryDateInside

class MainPage(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            user = users.get_current_user()
            url_linktext = 'Logout'
            template_values = {
                'url': url,
                'user' :user,
                'url_linktext': url_linktext
            }

            path = os.path.join(os.path.dirname(__file__), 'webpages/index1.html')
            self.response.out.write(template.render(path, template_values))
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            template_values = {
                'url': url,
                'url_linktext': url_linktext
            }

            path = os.path.join(os.path.dirname(__file__), 'webpages/index2.html')
            self.response.out.write(template.render(path, template_values))

        
        
application = webapp.WSGIApplication(
                                     [('/',MainPage),
                                      ('/mainMenu',MainMenu),
                                      ('/itemsOfUser',ItemsOfUser),
                                      ('/addItem',addItem),
                                      ('/voteItems',VoteItems),
                                      ('/castVote',castVote),
                                      ('/resultsPage',resultsPage),
                                      ('/exportXML',exportXML),
                                      ('/importXML',importXML),
                                      ('/editCategories',editCategories),
                                      ('/renameCategory',renameCategory),
                                      ('/renameCategoryInside',renameCategoryInside),
                                      ('/deleteCategory',deleteCategory),
                                      ('/deleteCategoryInside',deleteCategoryInside),
                                      ('/renameItem',renameItem),
                                      ('/renameItemInside',renameItemInside),
                                      ('/renameItemInside2',renameItemInside2),
                                      ('/deleteItem',deleteItem),
                                      ('/deleteItemInside',deleteItemInside),
                                      ('/search',search),
                                      ('/expiryDate',expiryDate),
                                      ('/expiryDateInside',expiryDateInside)],
                                         debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
