from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.db import BadKeyError
from google.appengine.ext.webapp import RequestHandler, template
from logic.models import PerformanceReview

class GetManagerForm(RequestHandler):

    template_values = {}
    path = 'templates/api.manager_form.html'

    def get(self, key):

        user = self.request.environ['current_user']

        type = 'manager'

        login_url = users.create_login_url(self.request.uri)
        logout_url = users.create_logout_url(login_url)

        try:
            pr = PerformanceReview.get(key)
        except BadKeyError:
            self.error(405)
            return

        form = pr.manager_form

        prev_pr = PerformanceReview.all().order('-date').\
                                        filter('date <', pr.date).\
                                        filter('employee', pr.employee).get()

        data = form.get_all_data

        upload_url = blobstore.create_upload_url('/upload')

        self.template_values.update({'form': form,
                                     'file_key': form.file_key,
                                     'user': user,
                                     'upload_url': upload_url,
                                     'prev_pr': prev_pr,
                                     'file_name': form.file_name})

        self.response.out.write(template.render(self.path,
                                                self.template_values))
