from google.appengine.ext.db import Model
from google.appengine.ext.webapp import RequestHandler, template
from logic.models import User

class GetManagers(RequestHandler):

    def get(self):

        users = User.all()
        managers = []
        for user in users:
            for role in user.role:
                if Model.get(role).value == 'manager':
                    managers.append(user)

        template_values = {'managers': managers,
                           }

        path = 'templates/new_user.html'
        self.response.out.write(template.render(path, template_values))