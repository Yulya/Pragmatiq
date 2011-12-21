import logging
import urllib
from google.appengine.ext.webapp import RequestHandler, template
from logic.models import PerformanceReview, SharedForm, Dept


class GetPrs(RequestHandler):

    #selects all PR objects for current user's subs and returns them
    def get(self, dept):

        user = self.request.environ['current_user']
        dept = urllib.unquote(dept).decode('utf-8')

        def get_sub_prs(manager, prs):

            logging.debug('manager %s' % manager.email)
            current_manager_prs = PerformanceReview.all().filter('manager',
                                             manager).order("-date").fetch(1000)
            for pr in current_manager_prs:
                logging.debug('current %s' %pr.employee.email)

            prs.extend(current_manager_prs)

            for pr in prs:
                logging.debug(': %s' %pr.employee.email)

            for manager in manager.subs:
                get_sub_prs(manager, prs)


            return prs

        prs = PerformanceReview.all().filter('manager',
                                             user).order("-date").fetch(1000)

#        for pr in prs:
#            logging.debug('1: %s' % pr.employee.email)

        if user.edit_sub_reviews:
            prs = []
            get_sub_prs(user, prs)
#
#        for pr in prs:
#            logging.debug('2: %s' %pr.employee.email)

        if dept == 'all':

            departments = Dept.all().fetch(1000)

            for department in departments:
                department.prs = filter(lambda x: x.employee.dept.name
                == department.name, prs)
                logging.debug(department.prs)

        else:
            departments = Dept.all().filter('name', dept).fetch(1000)

            for department in departments:
                department.prs = filter(lambda x: x.employee.dept.name
                == department.name, prs)

        shared_forms = SharedForm.all().filter('user', user).fetch(1000)

        template_values = {'dept': dept,
                           'depts': departments,
                           'current_user': user.email,
                           'shared_forms': shared_forms}

        path = 'templates/api.manager.html'
        self.response.out.write(template.render(path, template_values))
