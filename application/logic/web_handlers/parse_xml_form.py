import datetime
import logging
import urllib
from xml.etree import ElementTree
from google.appengine.ext.blobstore import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from logic.models import PerformanceReviewPeriod, \
    PerformanceReview, User, Achievements, PerformanceReviewForm,\
    Challenges, NextGoals

class ParseXml(blobstore_handlers.BlobstoreUploadHandler):
    
    def get(self, role, pr_key, blob_key):

        blob_key = str(urllib.unquote(blob_key))
        blob_info = blobstore.BlobInfo.get(blob_key)

        current_pr = PerformanceReview.get(pr_key)

        if role == 'manager':
            url = '/#/manager/pr/get/manager/%s' %current_pr.key()
        elif role == 'hr':
            url = '/#/hr/get/manager/%s' %current_pr.key()
        elif role == 'employee':
            url = '/#/employee/pr/get/employee/%s' %current_pr.key()
        else:
            url = '/'

        file = blob_info.open()

        employee = current_pr.employee

        NAMESPACES = {
            'w':"http://schemas.microsoft.com/office/word/2003/wordml",
            'v':"urn:schemas-microsoft-com:vml",
            'w10':"urn:schemas-microsoft-com:office:word",
            'sl':"http://schemas.microsoft.com/schemaLibrary/2003/core",
            'aml':"http://schemas.microsoft.com/aml/2001/core",
            'wx':"http://schemas.microsoft.com/office/word/2003/auxHint",
            'o':"urn:schemas-microsoft-com:office:office",
            'dt':"uuid:C2F41010-65B3-11d1-A29F-00AA00C14882",
            'wsp':"http://schemas.microsoft.com/office/word/2003/wordml/sp2",
            'ns0':"GD_AssessmentReportManager.xsl",
        }

        ElementTree.register_namespace(
                                'o',
                                'urn:schemas-microsoft-com:office:office')

        try:
            parser = ElementTree.parse(file)
        except SyntaxError:
            self.response.out.write('incorrect type')
            return

        date = parser.find('.//w:body//ns0:ActionDateFormat//w:t',
                          namespaces=NAMESPACES).text
        manager_type = parser.find(
                          './/w:body//ns0:GD_ManagerAssessmentForm//w:t',
                          namespaces=NAMESPACES)
        if manager_type is None:

            blob_info.delete()
            self.response.out.write('incorrect type')
#
            return

        fio = parser.find('.//w:body//ns0:EmployeeName//w:t',
                          namespaces=NAMESPACES).text.replace('  ',' ').strip()

        last_name, first_name = fio.split(' ')[:2]

        employee_from_form = User.gql(
            "WHERE last_name = :last_name AND first_name = :first_name",
                                      last_name=last_name,
                                      first_name=first_name).get()

        if employee_from_form is None or \
            employee_from_form.email != employee.email:

            blob_info.delete()
            self.response.out.write('incorrect user')
            return

        date = datetime.datetime.strptime(date, '%d/%m/%Y').date()
        type = 'annual'
        description = "PR %s: %s-%s" % (type, date, date)

        month = datetime.timedelta(days=30)

        period = PerformanceReviewPeriod.gql("WHERE start_date >= \
                                            :min_start_date AND \
                                            start_date <= :max_start_date",
                                             max_start_date=date+month,
                                             min_start_date=date-month).get()
        if period is None:
            period = PerformanceReviewPeriod(start_date=date,
                                             finish_date=date,
                                             description=description,
                                             type=type)
            period.put()

        pr = PerformanceReview(employee=employee,
                               first_effective_date=employee.first_date,
                               manager=employee.manager,
                               period=period,
                               date=date)
        pr.put()

        manager_form = PerformanceReviewForm(pr=pr,
                                             status='approved',
                                     type='manager')
        manager_form.put()

        achievements = parser.findall(
                    './/w:body//ns0:AchievementMngList//ns0:Description//w:t',
                    namespaces=NAMESPACES)

        for achievement in achievements:

            achievement = achievement.text.replace('\n', '').replace('  ',' ')

            logging.debug(achievement)
            ach = Achievements(value=achievement,
                               form=manager_form)
            ach.put()

        challenges = parser.findall(
                    './/w:body//ns0:ChallengeMngList//ns0:Description//w:t',
                    namespaces=NAMESPACES)

        for challenge in challenges:

            challenge = challenge.text.replace('\n', '').replace('  ',' ')
            ch = Challenges(value=challenge,
                               form=manager_form)
            ch.put()

        goals = parser.findall(
                    './/w:body//ns0:NextYearGoalsMng//ns0:Goal//w:t',
                    namespaces=NAMESPACES)
        
        for goal in goals:

            goal = goal.text.replace('\n', '').replace('  ',' ')
            g = NextGoals(value=goal,
                               form=manager_form)
            g.put()

        blob_info.delete()
        self.response.out.write('done')


