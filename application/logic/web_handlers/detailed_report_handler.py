import datetime
from google.appengine.ext.webapp import RequestHandler, template
from logic.func import get_prev_pr
from logic.models import PerformanceReview

class GetDetailedReport(RequestHandler):

    def get(self):

        prs = PerformanceReview.all().fetch(1000)

        prs = filter(lambda x: x.period.finish_date > datetime.date.today(),
                     prs)
        prs = sorted(prs, key=lambda x: x.employee.dept.name)

        for pr in prs:
            if get_prev_pr(pr):
                try:
                    if get_prev_pr(pr).manager_form.get_all_data['salary'].\
                       value != pr.manager_form.get_all_data['salary'].value:
                        pr.salary_highlight = 'highlight'

                    if get_prev_pr(pr).manager_form.get_all_data['grade'].\
                        value != pr.manager_form.get_all_data['grade'].value:
                        pr.grade_highlight = 'highlight'
                except AttributeError:
                    pr.grade_highlight = None

        path = 'templates/detailed_report.html'
        self.response.out.write(template.render(path, {'prs': prs}))
  