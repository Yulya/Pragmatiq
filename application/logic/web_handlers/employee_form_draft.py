from logic.web_handlers.employee_form_submit_handler import EmployeeFormSubmit


class EmployeeFormDraft(EmployeeFormSubmit):

    status = 'draft'

    def get(self, key):

        super(EmployeeFormDraft, self).get(key)
