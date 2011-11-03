from google.appengine.api.datastore_errors import BadKeyError
from google.appengine.ext.webapp import RequestHandler
from logic.models import PerformanceReview

class RegisterPerformanceReview(RequestHandler):

    def post(self):

        keys = self.request.get('keys')[:-1].split(',')

        for key in keys:
            try:
                pr = PerformanceReview.get(key)
                manager_form = pr.manager_form
                manager_form.status = 'registered'
                manager_form.put()
            except BadKeyError, AttributeError:
                self.error(404)

        self.response.out.write('ok')