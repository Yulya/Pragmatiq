import logging
from google.appengine.ext.webapp import RequestHandler, template
from logic.models import PerformanceReviewPeriod


class HRHome(RequestHandler):

    def get(self):

        open_periods = PerformanceReviewPeriod.all().order("-start_date").filter('is_open', True).fetch(1000)
        closed_periods = PerformanceReviewPeriod.all().order("-start_date").filter('is_open', False).fetch(1000)

        for period in open_periods:
            period.register = 'disabled'
            period.delete = 'inline'
            period.pr = []
            for pr in period.performance_reviews:
                if pr.manager_form or pr.employee_form:
                    period.delete = 'none'
                pr.register = 'disabled'
                if pr.manager_form:
                    if pr.manager_form.status == 'submitted':
                        period.register = ''
                        pr.register = ''
                period.pr.append(pr)

        template_values = {'open_periods': open_periods,
                           'closed_periods': closed_periods}

        path = 'templates/hr_table.html'
        self.response.out.write(template.render(path, template_values))
