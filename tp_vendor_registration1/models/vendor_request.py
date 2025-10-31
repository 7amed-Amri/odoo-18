from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class VendorRequest(models.Model):
    _name = 'vendor.request'
    _description = 'Vendor Registration Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    _rec_name = 'name'

    name = fields.Char(
        string='Vendor Name', 
        required=True, 
        tracking=True,
        help="Name of the vendor contact person"
    )
    email = fields.Char(
        string='Email', 
        required=True, 
        tracking=True,
        help="Email address of the vendor"
    )
    phone = fields.Char(
        string='Phone', 
        tracking=True,
        help="Phone number of the vendor"
    )
    company_name = fields.Char(
        string='Company Name', 
        required=True, 
        tracking=True,
        help="Name of the vendor company"
    )
    
    # Address fields
    street = fields.Char(string='Street', tracking=True)
    city = fields.Char(string='City', tracking=True)
    zip = fields.Char(string='ZIP Code', tracking=True)
    country_id = fields.Many2one(
        'res.country', 
        string='Country', 
        tracking=True
    )
    
    # Status and workflow
    status = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', tracking=True, required=True)
    
    partner_id = fields.Many2one(
        'res.partner', 
        string='Created Partner', 
        readonly=True, 
        tracking=True,
        help="Partner record created upon approval"
    )
    
    # Department support
    department = fields.Selection([
        ('procurement', 'Procurement'),
        ('it', 'IT'),
        ('marketing', 'Marketing'),
        ('operations', 'Operations'),
        ('finance', 'Finance'),
        ('hr', 'Human Resources'),
        ('other', 'Other')
    ], string='Department', help="Related department for this vendor")
    
    department_notes = fields.Text(
        string='Department Notes',
        help="Additional notes related to the department"
    )
    
    # Additional fields
    website = fields.Char(string='Website')
    tax_id = fields.Char(string='Tax ID')
    business_type = fields.Selection([
        ('individual', 'Individual'),
        ('company', 'Company'),
        ('partnership', 'Partnership'),
        ('corporation', 'Corporation')
    ], string='Business Type', default='company')
    
    # Computed fields
    partner_count = fields.Integer(
        string='Partner Count',
        compute='_compute_partner_count'
    )
    
    @api.depends('partner_id')
    def _compute_partner_count(self):
        for record in self:
            record.partner_count = 1 if record.partner_id else 0
    
    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email and '@' not in record.email:
                raise ValidationError(_('Please enter a valid email address.'))
    
    def action_submit(self):
        """Submit the vendor request"""
        self.write({'status': 'submitted'})
        self.message_post(
            body=_('Vendor request has been submitted for review.'),
            message_type='notification'
        )
    
    def action_approve(self):
        """Approve the vendor request and create partner"""
        for record in self:
            if record.status != 'submitted':
                continue
                
            # Create partner
            partner_vals = {
                'name': record.company_name,
                'email': record.email,
                'phone': record.phone,
                'street': record.street,
                'city': record.city,
                'zip': record.zip,
                'country_id': record.country_id.id if record.country_id else False,
                'website': record.website,
                'vat': record.tax_id,
                'is_company': True,
                'supplier_rank': 1,
                'customer_rank': 0,
                'comment': f'Created from vendor request: {record.name}',
            }
            
            partner = self.env['res.partner'].create(partner_vals)
            
            # Update request
            record.write({
                'status': 'approved',
                'partner_id': partner.id
            })
            
            record.message_post(
                body=_('Vendor request approved. Partner %s created.') % partner.name,
                message_type='notification'
            )
            
        return True
    
    def action_reject(self):
        """Reject the vendor request"""
        self.write({'status': 'rejected'})
        self.message_post(
            body=_('Vendor request has been rejected.'),
            message_type='notification'
        )
    
    def action_reset_to_draft(self):
        """Reset to draft status"""
        self.write({'status': 'draft'})
        self.message_post(
            body=_('Vendor request reset to draft.'),
            message_type='notification'
        )
    
    def action_view_partner(self):
        """Smart button to view created partner"""
        self.ensure_one()
        if not self.partner_id:
            return False
            
        return {
            'type': 'ir.actions.act_window',
            'name': _('Vendor Partner'),
            'res_model': 'res.partner',
            'res_id': self.partner_id.id,
            'view_mode': 'form',
            'target': 'current',
        }
