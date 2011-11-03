from google.appengine.api import users
from google.appengine.ext.webapp import RequestHandler

class UrlHandler(RequestHandler):

    def get(self):

        login_url = users.create_login_url('/')
        logout_url = users.create_logout_url(login_url)
        self.redirect(logout_url)