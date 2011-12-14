from google.appengine.ext.webapp import template
from logic.web_handlers.base_form_handler import BaseFormHandler


class HRManagerForm(BaseFormHandler):

    template_values = {}
    path = 'templates/api.hr_maf.html'
    type = 'manager'

    def get(self, key):
        super(HRManagerForm, self).get(key)

        if self.template_values['form'].status == 'draft':
            self.response.out.write('form is in work')
            return

        self.response.out.write(template.render(self.path,
                                                self.template_values))
