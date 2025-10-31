from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EmployeeSheet(models.Model):
    _inherit = 'hr.employee'

    from_date = fields.Datetime(string="From Date")
    to_date = fields.Datetime(string="To Date")
    total_days = fields.Integer(string="Total Days", compute='_compute_total_days', store=True)
    custom_char = fields.Char(string="Custom Field", default='test')

    # Compute total_days
    @api.depends('from_date', 'to_date')
    def _compute_total_days(self):
        for rec in self:
            if rec.from_date and rec.to_date:
                if rec.to_date < rec.from_date:
                    raise ValidationError("End date cannot be before start date!")
                rec.total_days = (rec.to_date - rec.from_date).days
            else:
                rec.total_days = 0

    # Ensure char is filled
    @api.model
    def create(self, vals):
        if not vals.get('custom_char'):
            vals['custom_char'] = 'test'
        return super().create(vals)

    def write(self, vals):
        if 'custom_char' in vals and not vals['custom_char']:
            vals['custom_char'] = 'test'
        return super().write(vals)
