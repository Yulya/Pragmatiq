from google.appengine.ext.webapp import RequestHandler
from logic.models import PerformanceReviewForm

class EmployeeFormSubmit(RequestHandler):

    status = 'submitted'
    redirect_url = '/'

    def get(self, key):

        user = self.request.environ['current_user']

        form = PerformanceReviewForm.get(key)

        form.status = self.status
        form.put()

        self.response.out.write('ok')