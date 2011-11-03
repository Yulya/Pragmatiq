from google.appengine.ext.webapp import RequestHandler
from logic.models import PerformanceReviewForm

class ManagerFormApprove(RequestHandler):

    def get(self, key):

        user = self.request.environ['current_user']

        form = PerformanceReviewForm.get(key)

        if form.pr.manager.email != user.email:
            self.error(307)
            return

        if form.status == 'registered':
            form.status = 'approved'
            form.put()