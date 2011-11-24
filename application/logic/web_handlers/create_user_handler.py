from google.appengine.ext.db import Model
from google.appengine.api.datastore_errors import BadKeyError
from google.appengine.ext.webapp import RequestHandler
from logic.models import Dept, User, Role

class CreateUser(RequestHandler):

    #gets data and puts them to DB

    def post(self):

        first_name = self.request.get('first_name').strip()
        login = self.request.get('login').strip()
        email = self.request.get('email').strip()
        last_name = self.request.get('last_name').strip()
        dept = self.request.get('dept')
        position = self.request.get('position')

        dept_ref = Dept.all().filter('name', dept).get()

        if dept_ref is None:
            dept_ref = Dept(name=dept)
            dept_ref.put()

        try:
            manager = Model.get(self.request.get('manager'))
        except BadKeyError:
            manager = None

        roles = self.request.get('role')[:-1].split(',')
        if User.all().filter('login', login).get() is None:

            try:
                user = User(login=login,
                            first_name=first_name,
                            email=email,
                            last_name=last_name,
                            dept=dept_ref,
                            position=position,
                            manager=manager)

                for role in roles:
                    role_key = Role.gql("WHERE value = :role",
                                        role=role).get().key()
                    user.role.append(role_key)

                user.put()
            except ValueError:
                self.response.out.write('error')
                return
            self.response.out.write('ok')
        else: self.response.out.write('user with this login already exist')
