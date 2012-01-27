from google.appengine.ext.webapp import template
from logic.web_handlers.base_form_handler import BaseFormHandler


class ManagerEmployeeForm(BaseFormHandler):

    template_values = {}
    path = 'templates/api.manager_eaf.html'
    type = 'employee'

    def get(self, key):

        super(ManagerEmployeeForm, self).get(key)

        self.response.out.write(template.render(self.path,
                                                self.template_values))
