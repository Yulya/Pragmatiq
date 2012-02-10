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

            period.prs = period.performance_reviews.fetch(1000)
            for pr in period.prs:
                if pr.period.is_open:
                    if not pr.employee.dept.key() in period.departments:
                        period.departments.append(pr.employee.dept.key())
            period.departments = map(lambda x: Dept.get(x), period.departments)

            for pr in period.prs:
                if pr.manager_form or pr.employee_form:
                    period.delete = 'none'
                pr.register = 'disabled'

            for department in period.departments:
                department.register = 'disabled'
                department.prs = filter(lambda x: x.employee.dept.name == department.name, period.prs)
                for pr in department.prs:
                    if pr.manager_form:
                        if pr.manager_form.status == 'submitted':
                            department.register = ''
                            pr.register = ''

        template_values = {'open_periods': open_periods,
                           'closed_periods': closed_periods}

        path = 'templates/hr_table.html'
        self.response.out.write(template.render(path, template_values))
