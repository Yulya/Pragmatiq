from google.appengine.ext.webapp import template
from logic.web_handlers.base_form_handler import BaseFormHandler

class GetManagerForm(BaseFormHandler):

    template_values = {}
    path = 'templates/api.manager_form.html'
    type = 'manager'

    def get(self, key):

        super(GetManagerForm, self).get(key)

        if self.template_values['form'].status == 'submitted':
            self.response.out.write('form is temporary unavailable')
            return

        if self.template_values['form'].status == 'registered':
            self.path = 'templates/api.registered_maf.html'
            
        self.response.out.write(template.render(self.path,
                                                self.template_values))
