from logic.web_handlers.employee_form_submit_handler import EmployeeFormSubmit


class ManagerFormRegister(EmployeeFormSubmit):

    status = 'registered'

    def get(self, key):

        super(ManagerFormRegister, self).get(key)
