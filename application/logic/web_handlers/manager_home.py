from google.appengine.ext.webapp import RequestHandler, template
from logic.models import PerformanceReviewPeriod

class ManagerHome(RequestHandler):

    #show home page
    def get(self):
        manager = self.request.environ['current_user']

        user_departments = list()
        user_departments.append(manager.dept)

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
