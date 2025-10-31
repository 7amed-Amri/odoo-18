from odoo import models, fields

class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    sheet_code = fields.Char(string="Sheet Code")
    sheet_notes = fields.Text(string="Employee Sheet Notes")

    def action_open_contacts(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Contacts',
            'res_model': 'hr.employee.sheet.wizard',  # must be correct key and value
            'view_mode': 'form',
            'target': 'new',
        }
