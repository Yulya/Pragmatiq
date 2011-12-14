from logic.web_handlers.employee_form_submit_handler import EmployeeFormSubmit


class ManagerFormApprove(EmployeeFormSubmit):

    status = 'approved'

    def get(self, key):

        super(ManagerFormApprove, self).get(key)
