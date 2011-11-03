from google.appengine.ext.webapp import RequestHandler
from logic.models import PerformanceReviewForm

class EmployeeFormSubmit(RequestHandler):

    def get(self, key):

        user = self.request.environ['current_user']

        form = PerformanceReviewForm.get(key)

        if form.pr.employee.email != user.email:
            self.error(307)
            return

        form.status = 'submitted'
        form.put()
        self.response.out.write('ok')