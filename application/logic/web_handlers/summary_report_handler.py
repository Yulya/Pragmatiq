import datetime
from google.appengine.ext.webapp import RequestHandler, template
from logic.models import Dept, PerformanceReviewPeriod

class GetSummaryReport(RequestHandler):

    def get(self, key):

        depts = Dept.all()
        period = PerformanceReviewPeriod.get(key)

        summary = []

        for dept in depts:

            existed_pr = filter(lambda x: x.self_pr.get(), dept.users)

            all_dept_prs = filter(lambda x: x.self_pr.filter('period', period).get(),
                                  existed_pr)
            employees = len(all_dept_prs)

            clean_manager_form = filter(lambda x:
                                        not x.self_pr.order('-date').get().
                                        manager_form,
                                        existed_pr)
            clean_employee_form = filter(lambda x:
                                         not x.self_pr.order('-date').get().
                                         employee_form,
                                         existed_pr)

            clean_draft = len(clean_employee_form) + len(clean_manager_form)

            not_clean_manager_form = filter(lambda x:
                                            x.self_pr.order('-date').get().
                                            manager_form,
                                            existed_pr)
            not_clean_employee_form = filter(lambda x:
                                             x.self_pr.order('-date').get().
                                             employee_form,
                                             existed_pr)

            man_draft_in_work = filter(lambda x:
                                       x.self_pr.order('-date').get().
                                       manager_form.status ==
                                       'draft',
                                       not_clean_manager_form)
            emp_draft_in_work = filter(lambda x:
                                       x.self_pr.order('-date').get().
                                       employee_form.status ==
                                       'draft', not_clean_employee_form)

            in_work = len(man_draft_in_work) + len(emp_draft_in_work)

            registered_pr = filter(lambda x:
                                   x.self_pr.order('-date').get().manager_form.
                                   status ==
                                   'registered', not_clean_manager_form)

            reg_pr = len(registered_pr)

            submitted_by_employee = filter(lambda x:
                                           x.self_pr.order('-date').get().
                                           employee_form.status
                                           == 'submitted',
                                           not_clean_employee_form)
            emp_submit = len(submitted_by_employee)

            submitted_by_manager = filter(lambda x:
                                          x.self_pr.order('-date').get().
                                          manager_form.status
                                          == 'submitted',
                                          not_clean_manager_form)
            man_submit = len(submitted_by_manager)

            approved_pr = filter(lambda x:
                                 x.self_pr.order('-date').get().manager_form
                                 .status ==
                                 'approved', not_clean_manager_form)

            approved = len(approved_pr)

            all_draft = clean_draft + in_work + emp_submit + man_submit

            percent = (approved*100)/employees

            dept_info = {'name': dept.name,
                         'employees': employees,
                         'clean': clean_draft,
                         'in_work': in_work,
                         'all_draft': all_draft,
                         'reg': reg_pr,
                         'percent': percent,
                         'approved': approved,
                         'emp_submit': emp_submit,
                         'man_submit': man_submit}

            summary.append(dept_info)

        template_values = {'summary': summary}

        path = 'templates/summary_report.html'
        self.response.out.write(template.render(path, template_values))