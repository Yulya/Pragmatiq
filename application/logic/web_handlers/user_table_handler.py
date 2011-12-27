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
        for user in users:
            user.roles = ''
            for role in user.role:
                user.roles = user.roles + Model.get(role).value + ' '
                
        upload_url_first_date = blobstore.create_upload_url('/upload_first_date')
        upload_url = blobstore.create_upload_url('/upload_contacts')




        self.template_values.update({'users': users,
                                     'upload_url_first_date': upload_url_first_date,
                                     'upload_url': upload_url})

        self.response.out.write(template.render(self.path,
                                                self.template_values))
