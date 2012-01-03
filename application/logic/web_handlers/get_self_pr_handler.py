from google.appengine.api.blobstore import blobstore
from google.appengine.ext.webapp import RequestHandler, template
from logic.models import PerformanceReview


class GetSelfPR(RequestHandler):

    def get(self):

        user = self.request.environ['current_user']

        pr = PerformanceReview.all().filter('employee', user).\
                                     order('-date').get()
        try:
            form = pr.employee_form
        except AttributeError:
            pr = None

        upload_url = blobstore.create_upload_url('/parse_form')

        template_values = {'pr': pr,
                            'user': user,
                          'upload_url': upload_url}

        path = 'templates/api.employee.html'
        self.response.out.write(template.render(path, template_values))
