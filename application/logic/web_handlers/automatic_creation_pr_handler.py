import datetime
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

        for employee in employees:
            if employee.first_date:
                if employee.first_date + 2 * month == today:

                    first_date = employee.first_date
                    start_date = first_date + datetime.timedelta(weeks=13)
                    finish_date = start_date + datetime.timedelta(weeks=2)
                    description = "%s %s first review" %(employee.first_name, employee.last_name)

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

            elif len(employee.self_pr.fetch(100)) > 0:
                last_pr = employee.self_pr.order('-date').get()
                last_pr_date = last_pr.period.start_date
                next_pr_start_date = last_pr_date + 6 * month
                next_pr_start_date = next_pr_start_date.replace(year=today.year)

                events = Event.all()

                next_date_near_event = 0
                create_event_today = None

                for event in events:
                    if event.start_date < today:
                        event.start_date = event.start_date.replace(year = (today.year + 1))
                        event.put()
                    delta = next_pr_start_date - event.start_date
                    if event.start_date - month == today or event.start_date.replace(year=(today.year + 1)):
                        create_event_today = event

                    if delta < month and delta > -month:
                        next_date_near_event = 1

                if not next_date_near_event:

                    if next_pr_start_date < today:
                        next_pr_start_date.replace(year=(today.year + 1))
                    if next_pr_start_date == today + month:
                        period = PerformanceReviewPeriod(start_date=next_pr_start_date,
                            description='self period',
                            finish_date=next_pr_start_date + 2 * week)
                        period.put()

                        pr = PerformanceReview(period=period,
                            employee=employee,
                            manager=employee.manager,
                            date=period.start_date
                        )
                        pr.put()

                elif create_event_today:

                    delta = next_pr_start_date - create_event_today.start_date

                    if delta < month and delta > -month:

                        description = 'aaa'
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


