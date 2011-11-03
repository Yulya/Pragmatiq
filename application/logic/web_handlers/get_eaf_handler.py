from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.db import BadKeyError
from google.appengine.ext.webapp import RequestHandler, template
from logic.func import get_prev_pr
from logic.models import PerformanceReview
from logic.web_handlers.base_form_handler import BaseFormHandler


class GetEmployeeForm(BaseFormHandler):

    template_values = {}
    path = 'templates/api.employee_form.html'
    type = 'employee'

    def get(self, key):

        super(GetEmployeeForm, self).get(key)

        self.response.out.write(template.render(self.path,
                                                self.template_values))
