from google.appengine.api.datastore_errors import BadKeyError
from google.appengine.ext.webapp import RequestHandler
from logic import models
from logic.models import PerformanceReviewForm


class AddData(RequestHandler):

    def post(self):

        dict = {'next_goals': 'NextGoals',
                'challenges': 'Challenges',
                'achievements': 'Achievements',
                'project': 'Project',
                'skill': 'Skill',
                'hr_comment': 'HrComment',
                'manager_comment': 'ManagerComment',
                'conclusion': 'Conclusion',
                'position': 'Position',
                'responsibility': 'Responsibility',
                'career': 'Career',
                'manager_help': 'ManagerHelp',
                'complaint': 'Complaint',
                'grade': 'Grade',
                'salary': 'Salary',
                'issue': 'Issue'}

        form_key = self.request.get('form_key')
        table = self.request.get('table')

        try:
            attr = getattr(models, dict[table])
        except AttributeError, KeyError:
            self.error(405)
            return

        obj = attr()

        try:
            obj.form = PerformanceReviewForm.get(form_key)
            obj.put()
            key = obj.key()
        except BadKeyError:
            self.error(405)
            return

        self.response.out.write(key)
