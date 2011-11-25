import datetime
from google.appengine.ext.webapp import RequestHandler
from logic.models import Event

class UpdateEvent(RequestHandler):

    def post(self):

        type = self.request.get('type')
        start = self.request.get('start')
        finish = self.request.get('finish')
        first_date = self.request.get('first_date')

        event = Event.all().filter('type', type).get()

        if event is None:
            event = Event()

        try:
            event.start_date = datetime.datetime.strptime(start,
                                                          '%Y-%m-%d').date()
        except ValueError:
            self.response.out.write('bad start date')
            return
        try:
            event.finish_date = datetime.datetime.strptime(finish,
                                                           '%Y-%m-%d').date()
        except ValueError:
            self.response.out.write('bad finish date')
            return
        try:
            event.first_effective_date = datetime.datetime.strptime(first_date,
                                                           '%Y-%m-%d').date()
        except ValueError:
            self.response.out.write('bad first effective date')
            return
        event.type = type
        event.put()
        self.response.out.write('ok')