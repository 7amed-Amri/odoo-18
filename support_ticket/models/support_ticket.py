from odoo import models, fields

class SupportTicket(models.Model):
    _name = "support.ticket"
    _description = "Support Ticket"

    name = fields.Char(string="Subject", required=True)
    email = fields.Char(string="Email", required=True)
    phone = fields.Char(string="Phone")
    description = fields.Text(string="Description")
    status = fields.Selection([
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string="Status", default='submitted')
    user_id = fields.Many2one('res.users', string="Assigned To")

    def action_approve(self):
        self.status = 'approved'

    def action_reject(self):
        self.status = 'rejected'
