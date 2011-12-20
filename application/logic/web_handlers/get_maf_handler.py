import datetime
from google.appengine.ext.webapp import template
from logic.web_handlers.base_form_handler import BaseFormHandler


class GetManagerForm(BaseFormHandler):

    template_values = {}
    path = 'templates/api.manager_form.html'
    type = 'manager'

    def get(self, key):

        super(GetManagerForm, self).get(key)

        form = self.template_values['form']
        user = self.template_values['user']

        if form.status == 'submitted':
            self.path = 'templates/api.readonly_maf.html'

        elif form.status == 'approved':
            self.path = 'templates/api.readonly_maf.html'

        elif form.status == 'registered':
            self.path = 'templates/api.registered_maf.html'

        current_time = datetime.datetime.now()

        if form.lock_time:
            if form.lock_time > current_time and \
               form.user_locked_form.email != user.email:
                self.path = 'templates/api.readonly_maf.html'

        self.response.out.write(template.render(self.path,
                                                self.template_values))
