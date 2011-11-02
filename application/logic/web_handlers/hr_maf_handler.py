from logic.web_handlers.get_maf_handler import GetManagerForm

class HRManagerForm(GetManagerForm):

    template_values = {}
    path = 'templates/api.hr_maf.html'

    def __init__(self):
        pass

    def get(self, key):
        super(HRManagerForm, self).get(key)
            


