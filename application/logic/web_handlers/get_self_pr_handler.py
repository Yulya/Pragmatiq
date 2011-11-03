from google.appengine.ext.webapp import RequestHandler
from logic.models import PerformanceReview

class GetSelfPR(RequestHandler):

    def get(self):

        user = self.request.environ['current_user']

        pr = PerformanceReview.all().filter('employee', user).\
                                     order('-date').get()
        try:
            form = pr.employee_form
        except AttributeError:
            self.response.out.write('pr not created')
            return
        if form is not None:
            self.response.out.write(pr.key())