import logging
from google.appengine.ext.webapp import RequestHandler, template
from logic.models import PerformanceReviewPeriod, Dept


class HRHome(RequestHandler):

    def get(self):

        open_periods = PerformanceReviewPeriod.all().order("-start_date").filter('is_open', True).fetch(1000)
        closed_periods = PerformanceReviewPeriod.all().order("-start_date").filter('is_open', False).fetch(1000)

        for period in open_periods:
            period.register = 'disabled'
            period.delete = 'inline'
            period.departments = []

            for pr in period.performance_reviews:
                if pr.period.is_open:
                    if not pr.employee.dept.key() in period.departments:
                        period.departments.append(pr.employee.dept.key())
            period.departments = map(lambda x: Dept.get(x), period.departments)

            for pr in period.performance_reviews:
                if pr.manager_form or pr.employee_form:
                    period.delete = 'none'
                pr.register = 'disabled'
                if pr.manager_form:
                    if pr.manager_form.status == 'submitted':
                        period.register = ''
                        pr.register = ''

            for department in period.departments:
                department.prs = filter(lambda x: x.employee.dept.name == department.name, period.performance_reviews)

        template_values = {'open_periods': open_periods,
                           'closed_periods': closed_periods}

        path = 'templates/hr_table.html'
        self.response.out.write(template.render(path, template_values))