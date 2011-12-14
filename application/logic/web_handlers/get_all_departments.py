from google.appengine.ext.webapp import RequestHandler, template
from logic.models import Dept


class HR(RequestHandler):

    def get(self):

        depts = Dept.all()

        template_values = {'depts': depts}

        path = 'templates/api.hr.html'
        self.response.out.write(template.render(path, template_values))
