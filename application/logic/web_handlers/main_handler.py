from google.appengine.api import users
from google.appengine.ext.db import Model
from google.appengine.ext.webapp import RequestHandler, template


class MainHandler(RequestHandler):

    #gets current user and returns his roles

    def get(self):

        user = self.request.environ['current_user']
        current_role = self.request.environ['current_role']
        email = None
        if user is not None:
            email = user.email

        login_url = users.create_login_url(self.request.uri)
        logout_url = users.create_logout_url(login_url)
        roles = []
        for role_key in user.role:
            roles.append(Model.get(role_key).value)
        template_values = {
                           'username': email,
                           'user': user,
                           'roles': roles,
                           'current_role': current_role,
                           'logout_url': logout_url}

        path = 'templates/index.html'
        self.response.out.write(template.render(path, template_values))
