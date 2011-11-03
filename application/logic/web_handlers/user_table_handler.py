from google.appengine.ext.db import Model
from google.appengine.ext.webapp import template, RequestHandler
from logic.models import User

class UserTable(RequestHandler):

    #selects all users and returns them
    path = 'templates/users.html'
    template_values = {}


    def get(self):
        users = User.all().fetch(1000)
        for user in users:
            user.roles = ''
            for role in user.role:
                user.roles = user.roles + Model.get(role).value + ' '

        self.template_values.update({'users': users})

#        path = 'templates/users.html'
        self.response.out.write(template.render(self.path, self.template_values))