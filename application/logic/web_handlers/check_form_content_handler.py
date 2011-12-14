from google.appengine.ext.webapp import RequestHandler
from logic.models import PerformanceReviewForm


class CheckFormContent(RequestHandler):

    def get(self, key):

        form = PerformanceReviewForm().get(key)
        unfilled_fields = []

        try:
            form.next_goals[0]
        except IndexError:
            unfilled_fields.append('next goals')
        try:
            form.challenges[0]
        except IndexError:
            unfilled_fields.append('challenges')
        try:
            form.projects[0]
        except IndexError:
            unfilled_fields.append('projects')
        try:
            form.skills[0]
        except IndexError:
            unfilled_fields.append('skills')
        try:
            form.responsibilities[0]
        except IndexError:
            unfilled_fields.append('responsibilities')
        try:
            form.careers[0]
        except IndexError:
            unfilled_fields.append('career')
        try:
            form.manager_helps[0]
        except IndexError:
            unfilled_fields.append('manager help')
        try:
            form.complaints[0]
        except IndexError:
            unfilled_fields.append('complaint')
        try:
            form.issues[0]
        except IndexError:
            unfilled_fields.append('issues')
        try:
            form.salary[0]
        except AttributeError:
            unfilled_fields.append('salary')
        try:
            form.grade[0]
        except AttributeError:
            unfilled_fields.append('grade')
        try:
            form.position[0]
        except AttributeError:
            unfilled_fields.append('position')
        try:
            form.conclusion[0]
        except AttributeError:
            unfilled_fields.append('conclusion')

        if unfilled_fields:
            self.response.out.write((',').join(unfilled_fields))
