import datetime
from google.appengine.ext.db import Model
from google.appengine.api.datastore_errors import BadKeyError
from google.appengine.ext.webapp import RequestHandler
from logic.models import Dept, User, Role


class CreateUser(RequestHandler):

    #gets data and puts them to DB

    def post(self):

        key = self.request.get('key')

        email = self.request.get('email').strip()

        if key:
            user = User.get(key)
        else:
            if User.all().filter('email', email).get() is not None:
                self.response.out.write('user with this login already exist')
                return
            user = User()

        user.email = email

        first_name = self.request.get('first_name').strip()
        user.first_name = first_name

        last_name = self.request.get('last_name').strip()
        user.last_name = last_name

        position = self.request.get('position')
        user.position = position

        first_date =  self.request.get('first_date')
        try:
            first_date = datetime.datetime.strptime(first_date, '%Y-%m-%d').date()
        except ValueError:
            first_date = None
        user.first_date = first_date

        dept = self.request.get('dept')
        dept_ref = Dept.all().filter('name', dept).get()

        if dept_ref is None:
            dept_ref = Dept(name=dept)
            dept_ref.put()

        user.dept = dept_ref
        try:
            manager = Model.get(self.request.get('manager'))
        except BadKeyError:
            manager = None
        user.manager = manager

        roles = self.request.get('role')[:-1].split(',')

        user.role = []
        for role in roles:
                role_key = Role.gql("WHERE value = :role",
                                    role=role).get().key()
                user.role.append(role_key)
        user.put()

        self.response.out.write('ok')
