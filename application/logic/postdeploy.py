from google.appengine.ext import db
from logic.models import Role


class PostDeployLog(db.Model):
    roles_deployed = db.BooleanProperty()


class PostDeploy():
    def __init__(self):
        self.deploy_log = self.__get_roles_deployed_object()

    def __get_roles_deployed_object(self):
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
            role = Role(value='manager')
            role.put()
            role = Role(value='employee')
            role.put()
            role = Role(value='hr')
            role.put()
            self.deploy_log.roles_deployed = True
            self.deploy_log.put()

    def post_deploy_routines(self):
        self.deploy_roles()
