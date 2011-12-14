from logic.web_handlers.employee_form_submit_handler import EmployeeFormSubmit


class ManagerFormDraft(EmployeeFormSubmit):

    status = 'draft'

    def get(self, key):

        super(ManagerFormDraft, self).get(key)
