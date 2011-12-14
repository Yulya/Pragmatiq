from logic.func import get_prev_pr
from logic.models import Salary, Grade, Position, Conclusion
from logic.web_handlers.add_form_handler import AddEmployeeForm


class AddManagerForm(AddEmployeeForm):

    type = "manager"
    form = None
    flag = 0

    def get(self, key):

        super(AddManagerForm, self).get(key)

        if self.form.type == 'manager':
            prev_pr = get_prev_pr(self.form.pr)
            try:
                prev_form = prev_pr.forms.filter('type', self.form.type).get()

                prev_salary = prev_form.get_all_data['salary']
                prev_grade = prev_form.get_all_data['grade']
            except AttributeError:
                prev_salary = None
                prev_grade = None

            prev_position = self.form.pr.employee.position

            if prev_salary:
                salary = Salary(value=prev_salary.value,
                                form=self.form)
            else:
                salary = Salary(value='N/A',
                                form=self.form)
            salary.put()

            if prev_grade:
                grade = Grade(value=prev_grade.value,
                      form=self.form)
            else:
                grade = Grade(value='N/A',
                      form=self.form)
            grade.put()

            if prev_position:
                position = Position(value=prev_position,
                                    form=self.form)
            else:
                position = Position(value='N/A',
                                    form=self.form)
            position.put()

            conclusion = Conclusion(value='meet expectation',
                                    form=self.form)
            conclusion.put()

            self.redirect('/manager/pr/get/%(type)s/%(key)s'
                            % {'type': self.type,
                               'key': self.form.pr.key()})
