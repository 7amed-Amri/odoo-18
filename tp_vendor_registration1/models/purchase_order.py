from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    vendor_request_ids = fields.One2many(
        'vendor.request',
        'partner_id',
        string='Related Vendor Requests',
        compute='_compute_vendor_requests',
        help="Vendor requests related to this partner"
    )
    
    vendor_request_count = fields.Integer(
        string='Vendor Requests Count',
        compute='_compute_vendor_requests'
    )
    
    @api.depends('partner_id')
    def _compute_vendor_requests(self):
        for order in self:
            if order.partner_id:
                vendor_requests = self.env['vendor.request'].search([
                    ('partner_id', '=', order.partner_id.id)
                ])
                order.vendor_request_ids = vendor_requests
                order.vendor_request_count = len(vendor_requests)
            else:
                order.vendor_request_ids = False
                order.vendor_request_count = 0
    
    def action_view_vendor_requests(self):
        """Action to view related vendor requests"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Related Vendor Requests',
            'res_model': 'vendor.request',
            'view_mode': 'list,form',
            'domain': [('partner_id', '=', self.partner_id.id)],
            'context': {'default_partner_id': self.partner_id.id},
        }
