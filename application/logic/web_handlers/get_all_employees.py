from google.appengine.ext.webapp import RequestHandler, template
from logic.models import PerformanceReviewPeriod


class GetAllEmployees(RequestHandler):

    def get(self):

        periods = PerformanceReviewPeriod.all().fetch(1000)

        for period in periods:
            period.register = 'disabled'
            period.pr = []
            for pr in period.performance_reviews:
                pr.register = 'disabled'
                if pr.manager_form:
                    if pr.manager_form.status == 'submitted':
                        period.register = ''
                        pr.register = ''
                period.pr.append(pr)

        template_values = {'periods': periods}

        path = 'templates/hr_table.html'
        self.response.out.write(template.render(path, template_values))
