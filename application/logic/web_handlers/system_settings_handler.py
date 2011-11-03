from google.appengine.ext.webapp import RequestHandler, template
from logic.models import Event

class GetSettings(RequestHandler):

    def get(self):

        events = Event.all()

        template_values = {'events': events}

        path = 'templates/settings.html'
        self.response.out.write(template.render(path, template_values))