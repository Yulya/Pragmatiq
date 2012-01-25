import urllib
from google.appengine.ext.webapp import RequestHandler, template
from logic.models import PerformanceReview, Dept, WorkProject, User, PerformanceReviewPeriod


class GetDepartmentPrs(RequestHandler):

    #selects all PR objects for current user's subs and returns them
    def get(self, name):

        user = self.request.environ['current_user']
        name = urllib.unquote(name).decode('utf-8')

        prs = PerformanceReview.all().filter('manager',
                                             user).order("-date").fetch(1000)

        def get_sub_prs(manager, prs):

            current_manager_prs = PerformanceReview.all().filter('manager',
                                             manager).order("-date").fetch(1000)

            prs.extend(current_manager_prs)

            for manager in manager.subs:
                get_sub_prs(manager, prs)


            return prs

        if user.edit_sub_reviews:
            prs = []
            get_sub_prs(user, prs)

        if name == 'all':
            departments = Dept.all().fetch(1000)
        else:
            departments = Dept.all().filter('name', name).fetch(1000)

        for department in departments:
            department.prs = filter(lambda x: x.employee.dept.name
            == department.name and x.period.is_open, prs)

        template_values = {'name': name,
                           'depts': departments,
                           'current_user': user.email}

        path = 'templates/api.manager.departments.html'
        self.response.out.write(template.render(path, template_values))
