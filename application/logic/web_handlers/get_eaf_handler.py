from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.db import BadKeyError
from google.appengine.ext.webapp import RequestHandler, template
from logic.func import get_prev_pr
from logic.models import PerformanceReview


class GetEmployeeForm(RequestHandler):

    def get(self, key):

        user = self.request.environ['current_user']

        type = 'employee'
        
        login_url = users.create_login_url(self.request.uri)
        logout_url = users.create_logout_url(login_url)

        try:
            pr = PerformanceReview.get(key)
        except BadKeyError:
            self.error(405)
            return

        form = pr.employee_form

        prev_pr = get_prev_pr(pr)

        try:
            prev_form = prev_pr.forms.filter('type', type).get()
        except AttributeError:
            prev_form = None
        try:
            prev_goals = prev_form.next_goals
        except AttributeError:
            prev_goals = []
        try:
            prev_challenges = prev_form.challenges
        except AttributeError:
            prev_challenges = []
        try:
            prev_achievements = prev_form.achievements
        except AttributeError:
            prev_achievements = []

        data = form.get_all_data

        upload_url = blobstore.create_upload_url('/upload')

        template_values = {'url': logout_url,
                           'key': form.key(),
                           'status': form.status,
                           'user': user,
                           'date': pr.date,
                           'emp': form.pr.employee,
                           'type': form.pr.period.type,
                           'file_key': form.file_key,
                           'file_name': form.file_name,
                           'upload_url': upload_url,
                           'prev_goals': prev_goals,
                           'prev_challenges': prev_challenges,
                           'prev_achievements': prev_achievements,
                           'data': data}

        path = 'templates/api.employee_form.html'
        self.response.out.write(template.render(path, template_values))
