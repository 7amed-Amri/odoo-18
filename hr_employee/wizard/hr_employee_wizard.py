from odoo import models, fields, api

class HrEmployeeSheetWizard(models.TransientModel):
    _name = 'hr.employee.sheet.wizard'
    _description = 'Employee Sheet Wizard'

    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    sheet_code = fields.Char(string="Sheet Code")
    sheet_notes = fields.Text(string="Notes")

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        active_id = self.env.context.get('active_id')
        if active_id:
            employee = self.env['hr.employee'].browse(active_id)
            res.update({
                'employee_id': employee.id,
                'sheet_code': employee.sheet_code,
                'sheet_notes': employee.sheet_notes,
            })
        return res

    def action_save_sheet(self):
        self.employee_id.write({
            'sheet_code': self.sheet_code,
            'sheet_notes': self.sheet_notes,
        })
        return {'type': 'ir.actions.act_window_close'}
