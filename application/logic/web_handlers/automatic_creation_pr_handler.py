import datetime
from google.appengine.ext.webapp import RequestHandler
from logic.models import PerformanceReview, PerformanceReviewPeriod, User,\
    Event


class AutomaticPerformanceReview(RequestHandler):

    def get(self):
        today = datetime.date.today()
        events = Event.all().filter('start_date', today)

        nearest_event = None
        #TODO: nearest_event_date
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

                last_pr = PerformanceReview.all().filter(
                                    'employee', employee).order('-date').get()

                if last_pr:
                    last_date = last_pr.date
                    month = datetime.timedelta(days=30)
                    review_next_date = last_date + 6 * month
                    delta = review_next_date - nearest_event.start_date
                    if delta <= month and delta >= -month:
                        if nearest_event.start_date == today:

                            pr = PerformanceReview(employee=employee,
                                                   manager=employee.manager,
                                                   first_effective_date=event.
                                                   first_effective_date,
                                                   date=period.start_date,
                                                   period=period)
                            pr.put()
                    else:
                        if review_next_date == today:
                            period = PerformanceReviewPeriod(type=nearest_event.type,
                                             description=description,
                                             start_date=event.start_date,
                                             finish_date=event.finish_date)
                            period.put()
                            pr = PerformanceReview(employee=employee,
                                                   manager=employee.manager,
                                                   first_effective_date=event.
                                                   first_effective_date,
                                                   date=period.start_date,
                                                   period=period)
                            pr.put()

