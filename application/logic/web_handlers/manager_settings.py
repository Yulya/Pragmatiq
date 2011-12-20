from google.appengine.ext.webapp import RequestHandler, template

class ManagerSettings(RequestHandler):

    def get(self):

        manager = self.request.environ['current_user']

        template_values = {'manager': manager}

        path = 'templates/manager.settings.html'
        self.response.out.write(template.render(path, template_values))