from google.appengine.ext.webapp import RequestHandler
from logic.models import PerformanceReviewPeriod

class ReopenPeriod(RequestHandler):

    def get(self, period_key):

        user = self.request.environ['current_user']

        period = PerformanceReviewPeriod.get(period_key)

        if not period.is_open:
            period.is_open = True
            period.put()
        else:
            self.response.out.write('Error. Period is opened')
            return
        
        self.response.out.write('ok')

