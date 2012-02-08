from google.appengine.ext.db import Model
from google.appengine.ext.webapp import RequestHandler, template
from logic.models import User, Dept, Role


class UserData(RequestHandler):

    def get(self, key):

        users = User.all()
        managers = []
        for user in users:
            for role in user.role:
                if Model.get(role).value == 'manager':
                    managers.append(user)

        roles = []
        if key:
            user = User.get(key)
            for role in user.role:
                roles.append(Role.get(role).value)
        else:
            user = None

        template_values = {'managers': managers,
                           'user': user,
                           'roles': roles}

        path = 'templates/new_user.html'
        self.response.out.write(template.render(path, template_values))
