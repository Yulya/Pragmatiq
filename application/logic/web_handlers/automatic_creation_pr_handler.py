import datetime
import logging
from google.appengine.ext.webapp import RequestHandler
from logic.models import PerformanceReview, PerformanceReviewPeriod, User,\
    Event


class AutomaticPerformanceReview(RequestHandler):

    def get(self):
        today = datetime.date.today()
        events = Event.all()
        employees = User.all()
        month = datetime.timedelta(days=30)
        week = datetime.timedelta(weeks=1)

        for event in events:

            if event.start_date < today:
                event.start_date = event.start_date.replace(year = (today.year + 1))
                event.put()

        for employee in employees:

            first_date = employee.first_date

            start_date = first_date + datetime.timedelta(weeks=13)
            finish_date = start_date + datetime.timedelta(weeks=2)

            if start_date - month == today:

                description = "PR annual: %s-%s" % (start_date, finish_date)

                period = PerformanceReviewPeriod(type='annual',
                                                description=description,
                                                start_date=start_date,
                                                finish_date=finish_date)
                period.put()

                pr = PerformanceReview(employee=employee,
                                        manager=employee.manager,
                                        date=period.start_date,
                                        period=period)
                pr.put()

            if employee.self_pr.fetch(100):
                
                last_pr = employee.self_pr.order('-date').get()
                last_pr_date = last_pr.period.start_date
                next_pr_start_date = last_pr_date + 6 * month

            else:
                next_pr_start_date = None

            if next_pr_start_date:



                for event in events:

                    delta = next_pr_start_date - event.start_date
                    event_for_pr = None
                    if delta < month and delta > -month:
                        event_for_pr = event

                    if event_for_pr:
                        logging.debug(event_for_pr.start_date - month)
                        if event_for_pr.start_date - month == today:


                            description = "PR %s: %s-%s" % (event_for_pr.type, event_for_pr.start_date, event_for_pr.finish_date)
                            period = PerformanceReviewPeriod(start_date=event_for_pr.start_date,
                                description=description,
                                finish_date=event_for_pr.finish_date)
                            period.put()

                            pr = PerformanceReview(period=period,
                                employee=employee,
                                manager=employee.manager,
                                date=period.start_date
                            )
                            pr.put()
                    else:

                        if next_pr_start_date == today + month:
                            finish_date = next_pr_start_date + 2 * week
                            description = "PR custom: %s-%s" % (next_pr_start_date, finish_date)
                            period = PerformanceReviewPeriod(start_date=next_pr_start_date,
                                description='self period',
                                finish_date=finish_date)
                            period.put()

                            pr = PerformanceReview(period=period,
                                employee=employee,
                                manager=employee.manager,
                                date=period.start_date
                            )
                            pr.put()

            else:

                for event in events:
                    if event.start_date - month == today or event.start_date.replace(year=(today.year + 1)):

                        description = "PR %s: %s-%s" % (event.type, event.start_date, event.finish_date)
                        period = PerformanceReviewPeriod(start_date=event.start_date,
                            description=description,
                            finish_date=event.finish_date)
                        period.put()

                        pr = PerformanceReview(period=period,
                            employee=employee,
                            manager=employee.manager,
                            date=period.start_date
                        )
                        pr.put()
