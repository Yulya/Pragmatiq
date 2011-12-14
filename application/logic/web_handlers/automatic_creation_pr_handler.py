import datetime
from google.appengine.ext.webapp import RequestHandler
from logic.models import PerformanceReview, PerformanceReviewPeriod, User,\
    Event


class AutomaticPerformanceReview(RequestHandler):

    def get(self):
        today = datetime.date.today()
        events = Event.all().filter('start_date', today)
        employees = User.all()
        for event in events:
            description = "PR %s: %s-%s" % (event.type,
                                            event.start_date,
                                            event.finish_date)

            period = PerformanceReviewPeriod(type=event.type,
                                             description=description,
                                             start_date=event.start_date,
                                             finish_date=event.finish_date)
            period.put()
            for employee in employees:
                pr = PerformanceReview(employee=employee,
                                       manager=employee.manager,
                                       first_effective_date=event.
                                       first_effective_date,
                                       date=period.start_date,
                                       period=period)
                pr.put()
