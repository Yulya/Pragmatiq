from logic.web_handlers.employee_form_submit_handler import EmployeeFormSubmit


class ManagerFormSubmit(EmployeeFormSubmit):

    status = 'submitted'

    def get(self, key):

        super(ManagerFormSubmit, self).get(key)
