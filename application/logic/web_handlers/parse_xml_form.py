import datetime
import logging
from xml.etree import ElementTree
from google.appengine.ext.webapp import blobstore_handlers
from logic.models import PerformanceReviewPeriod, PerformanceReview, User, Achievements, PerformanceReviewForm, Challenges, NextGoals

class ParseXml(blobstore_handlers.BlobstoreUploadHandler):
    
    def post(self):

        upload_files = self.get_uploads('file')
        blob_info = upload_files[0]

        file = blob_info.open()
        key = self.request.get('key')
        employee = User.get(key)


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

        ElementTree.register_namespace('o', 'urn:schemas-microsoft-com:office:office')

        parser = ElementTree.parse(file)

        date = parser.find('.//w:body//ns0:ActionDateFormat//w:t',
                          namespaces=NAMESPACES).text
        logging.debug(date)
        date = datetime.datetime.strptime(date, '%d/%m/%Y').date()
        type = 'annual'
        description = "PR %s: %s-%s" % (type, date, date)

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

        employee_form = PerformanceReviewForm(pr=pr,
                                              status='approved',
                                     type='employee')
        employee_form.put()
        manager_form = PerformanceReviewForm(pr=pr,
                                             status='approved',
                                     type='employee')
        manager_form.put()

        achievements = parser.findall('.//w:body//ns0:AchievementMngList//ns0:Description//w:t',
                              namespaces=NAMESPACES)
        for achievement in achievements:

            achievement = achievement.text.replace('\n', '').replace('  ',' ')

            logging.debug(achievement)
            ach = Achievements(value=achievement,
                               form=manager_form)
            ach.put()
            ach = Achievements(value=achievement,
                               form=employee_form)
            ach.put()

        challenges = parser.findall('.//w:body//ns0:ChallengeMngList//ns0:Description//w:t',
                              namespaces=NAMESPACES)
        for challenge in challenges:

            challenge = challenge.text.replace('\n', '').replace('  ',' ')
            ch = Challenges(value=challenge,
                               form=manager_form)
            ch.put()

            ch = Challenges(value=challenge,
                               form=employee_form)
            ch.put()

        goals = parser.findall('.//w:body//ns0:NextYearGoalsMng//ns0:Goal//w:t',
                              namespaces=NAMESPACES)
        for goal in goals:

            goal = goal.text.replace('\n', '').replace('  ',' ')
            g = NextGoals(value=goal,
                               form=manager_form)
            g.put()
            g = NextGoals(value=goal,
                               form=employee_form)
            g.put()

        self.redirect('/')


