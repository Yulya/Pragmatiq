import datetime
from google.appengine.ext.db import Model
from google.appengine.ext.webapp import RequestHandler
from logic.models import Role, PerformanceReviewPeriod, Comment, PerformanceReview, Salary

class CreatePR(RequestHandler):

    #creates PR objects for all employees

    def post(self):

        user = self.request.environ['current_user']

        role_key = Role.gql("WHERE value = :hr", hr='hr').get().key()

        if role_key not in user.role:
            self.error(403)
            return

        start_str = self.request.get('start')
        finish_str = self.request.get('finish')
        type = self.request.get('type')

        employees = self.request.get('employees')[:-1].split(',')

        try:
            start = datetime.datetime.strptime(start_str, '%Y-%m-%d').date()
            finish = datetime.datetime.strptime(finish_str, '%Y-%m-%d').date()
        except ValueError:
            self.response.out.write('incorrect date')
            self.error(403)
            return

        description = "PR %s: %s-%s" % (type, start_str, finish_str)

        period = PerformanceReviewPeriod(type=type,
                                         description=description,
                                         start_date=start,
                                         finish_date=finish)
        period.put()

        for employee in employees:
            comment = Comment()
            comment.put()
            if employee != '':
                user = Model.get(employee)
                pr = PerformanceReview(employee=user,
                                       comment=comment,
                                       manager=user.manager,
                                       period=period,
                                       date=start)
                pr.put()

        self.response.out.write('ok')