import datetime
from google.appengine.ext.webapp import RequestHandler
from logic.func import send_message
from logic.models import PerformanceReview


class CheckDate(RequestHandler):

    def get(self):

        today = datetime.date.today()
        subject = 'Performance Review'

        month = datetime.timedelta(days=30)
        week = datetime.timedelta(days=7)
        day = datetime.timedelta(days=1)

        prs = PerformanceReview.all().filter('start_date >=', today)

        for pr in prs:

            delta = pr.date - today
            text = 'Your Performance Review starts in ' \
                   + str(delta.days) + ' days'

            if delta == month or delta == week or delta == day:

                send_message(pr.employee.email, subject, text)
