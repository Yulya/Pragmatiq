from google.appengine.ext.webapp import RequestHandler, template
from logic.models import PerformanceReview, Role, CommentToForm


class EmployeeHome(RequestHandler):

    def get(self):

        user = self.request.environ['current_user']

        prs = PerformanceReview.gql("WHERE employee = :user ORDER BY date DESC", user = user)
        prs = prs.fetch(1000)

        user_is_manager = 0
        for role in user.role:
            if Role.get(role).value == "manager":
                user_is_manager = 1
                break

        current_pr = None

        comments = None

        if not user_is_manager:
            comments = CommentToForm.gql("WHERE manager = :manager AND comment = NULL", manager = user).fetch(1000)
            comments = filter(lambda x: x.pr.period.is_open, comments)
        if prs:
            if prs[0].period.is_open:
                current_pr = prs[0]
                prs.remove(prs[0])

        template_values = {'current_pr': current_pr,
                           'prs': prs,
                           'user': user,
                           'comments': comments
                        }

        path = 'templates/api.employee.html'
        self.response.out.write(template.render(path, template_values))
