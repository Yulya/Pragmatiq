from google.appengine.ext import db
from logic.models import Role, User, Dept


class PostDeployLog(db.Model):
    roles_deployed = db.BooleanProperty()
    users_deployed = db.BooleanProperty()


class PostDeploy():
    def __init__(self):
        self.deploy_log = self.__get_deployed_object()
        self.role_keys = {}

    def __get_deployed_object(self):
        query = PostDeployLog.all()
        if query.count() > 0:
            result = query.fetch(limit=1)
            deploy_log = result.pop()
            return deploy_log
        else:
            deploy_log = PostDeployLog()
            return deploy_log

    def deploy_roles(self):
        if not self.deploy_log.roles_deployed:
            manager_role = Role(value='manager')
            manager_role.put()
            employee_role = Role(value='employee')
            employee_role.put()
            hr_role = Role(value='hr')
            hr_role.put()
            self.deploy_log.roles_deployed = True
            self.deploy_log.put()
            self.role_keys.update({'manager': manager_role.key(),
                    'employee': employee_role.key(),
                    'hr': hr_role.key()})
            

    def deploy_users(self):
        if not self.deploy_log.users_deployed:

            roles = Role.all()

            dept = Dept(name='1')
            dept.put()

            first_user = User(first_name='Max',
                        last_name='Korenkov',
                        email='mkorenkov@mirantis.com',
                        position='manager',
                        manager=None,
                        role=[self.role_keys['manager'], self.role_keys['hr']],
                        dept=dept
                        )
            first_user.put()

            second_user = User(first_name='Yuliya',
                                last_name='Portnova',
                                email='jportnova@mirantis.com',
                                position='intern',
                                manager=first_user,
                                role=[self.role_keys['employee']],
                                dept=dept
                                )
            second_user.put()
            self.deploy_log.users_deployed = True
            self.deploy_log.put()

    def post_deploy_routines(self):
        self.deploy_roles()
        self.deploy_users()
