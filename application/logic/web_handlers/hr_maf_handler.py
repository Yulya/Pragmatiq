from logic.web_handlers.handlers import GetManagerForm

class HRManagerForm(GetManagerForm):

    template_values = {}
    path = 'templates/api.hr_maf.html'

    def __init__(self):
        pass

    def get(self, key):
        super(HRManagerForm, self).get(key)
            


