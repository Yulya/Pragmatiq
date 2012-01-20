import logging
from google.appengine.ext.webapp import RequestHandler, template
from logic.models import PerformanceReviewPeriod, Dept, PerformanceReview

class ManagerHome(RequestHandler):

    #show home page
    def get(self):
        manager = self.request.environ['current_user']

        user_departments = []

        prs = PerformanceReview.all().filter('manager',
                                             manager)

        for pr in prs:
            if pr.is_open:
                if not pr.employee.dept.key() in user_departments:
                    user_departments.append(pr.employee.dept.key())

        user_departments = map(lambda x: Dept.get(x), user_departments)

        last_pr = PerformanceReviewPeriod.gql("WHERE type in ('annual', 'semi-annual') ORDER BY finish_date DESC LIMIT 1").get()
        prs = PerformanceReviewPeriod.all().order("-finish_date").fetch(1000)
        current_pr = None

        if len(prs) > 0 and prs[0].key() == last_pr.key() and last_pr.is_open:
            current_pr = last_pr
            prs.remove(prs[0])

        template_values = {"departments": user_departments,
                           "projects": manager.projects,
                           "prs": prs,
                           "current_pr": current_pr
                           }

        path = 'templates/api.manager.home.html'
        self.response.out.write(template.render(path, template_values))
 