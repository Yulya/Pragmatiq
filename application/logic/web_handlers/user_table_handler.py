from google.appengine.api.blobstore import blobstore
from google.appengine.ext.db import Model
from google.appengine.ext.webapp import template, RequestHandler
from logic.models import User

class UserTable(RequestHandler):

    #selects all users and returns them
    path = 'templates/users.html'
    template_values = {}


    def get(self):
        users = User.all().fetch(1000)
        managers = []
        for user in users:
            user.roles = ''
            for role in user.role:
                if Model.get(role).value == 'manager':
                    if user not in managers:
                        managers.append(user)
                user.roles = user.roles + Model.get(role).value + ' '

        upload_url = blobstore.create_upload_url('/upload_contacts')
        
        managers.sort(key=lambda x: x.last_name)

        self.template_values.update({'users': users,
                                     'len_users': len(users),
                                     'len': len(managers),
                                     'managers': managers,
                                     'upload_url': upload_url})

        self.response.out.write(template.render(self.path, self.template_values))