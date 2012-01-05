import datetime
from google.appengine.ext.webapp import RequestHandler
from logic.func import send_message
from logic.models import PerformanceReview


class CheckDate(RequestHandler):

    def get(self):

        today = datetime.date.today()
        subject = 'Performance Review'

        two_weeks = datetime.timedelta(days=14)
        week = datetime.timedelta(days=7)

        prs = PerformanceReview.all().filter('start_date >=', today)

        for pr in prs:

            delta = pr.date - today
            text = 'Your Performance Review starts in ' \
                   + str(delta.days) + ' days'

            if delta == two_weeks or delta <= week:

                send_message(pr.employee.email, subject, text)
