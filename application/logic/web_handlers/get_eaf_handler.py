from google.appengine.ext.webapp import template
from logic.web_handlers.base_form_handler import BaseFormHandler


class GetEmployeeForm(BaseFormHandler):

    template_values = {}
    path = 'templates/api.readonly_eaf.html'
    type = 'employee'

    def get(self, key):

        super(GetEmployeeForm, self).get(key)

        user = self.template_values['user']
        employee = self.template_values['form'].pr.employee
        form = self.template_values['form']

        if form.status == 'draft':
            self.path = 'templates/api.employee_form.html'

        self.response.out.write(template.render(self.path,
                                                self.template_values))
