from odoo import models, fields, api

class CorrespondenceRecord(models.Model):
    _name = "correspondence.record"
    _description = "Correspondence Record"

    name = fields.Char(string="Subject", required=True)
    correspondence_type = fields.Selection(
        [
            ('incoming', 'Incoming'),
            ('outgoing', 'Outgoing'),
            ('internal', 'Internal'),
        ],
        string="Type",
        required=True,
        default='incoming'
    )
    reference_no = fields.Char(string="Reference No.")
    date = fields.Date(string="Date", default=fields.Date.today)
    sender = fields.Char(string="Sender")
    recipient = fields.Char(string="Recipient")
    description = fields.Text(string="Details")
    attachment_ids = fields.Many2many(
        'ir.attachment',
        string="Attachments"
    )