from google.appengine.ext.webapp import RequestHandler
from logic.models import PerformanceReviewPeriod

class DeletePR(RequestHandler):

    def post(self):

        period_key = self.request.get('period_key')

        if period_key:
            period = PerformanceReviewPeriod.get(period_key)

            delete_pr = 1
            for pr in period.performance_reviews:
                if pr.manager_form or pr.employee_form:
                    delete_pr = 0

            if delete_pr:
                for pr in period.performance_reviews:
                    pr.delete()
                period.delete()
