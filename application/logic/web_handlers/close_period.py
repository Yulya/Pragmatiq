from google.appengine.ext.webapp import RequestHandler
from logic.models import PerformanceReviewPeriod

class ClosePeriod(RequestHandler):

    def get(self, period_key):

        user = self.request.environ['current_user']

        period = PerformanceReviewPeriod.get(period_key)

        if period.is_open:
            period.is_open = False
            period.put()
        else:
            self.response.out.write('Error. Period is already closed')
            return
        
        self.response.out.write('ok')

