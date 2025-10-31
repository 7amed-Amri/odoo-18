from odoo import http
from odoo.http import request
import logging
import re

_logger = logging.getLogger(__name__)

class VendorRegistrationController(http.Controller):
    
    def _get_default_values(self):
        """Get default form values"""
        return {
            'name': '',
            'email': '',
            'phone': '',
            'company_name': '',
            'street': '',
            'city': '',
            'zip_code': '',
            'website': '',
            'tax_id': '',
            'department': '',
            'department_notes': '',
            'business_type': 'company',
            'country_id': '',
        }
    
    def _validate_email(self, email):
        """Simple email validation"""
        if not email:
            return False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @http.route(['/vendor-registration'], type='http', auth="public", website=True)
    def vendor_registration_form(self, **kwargs):
        """Display vendor registration form"""
        countries = request.env['res.country'].sudo().search([])
        
        # Start with default values
        values = self._get_default_values()
        values.update({
            'countries': countries,
            'error': {},
            'error_message': [],
        })
        
        # Pre-fill form if data exists in kwargs
        for field in values.keys():
            if field in ['countries', 'error', 'error_message']:
                continue
            if field == 'zip_code' and 'zip' in kwargs:
                values['zip_code'] = kwargs['zip']
            elif field in kwargs:
                values[field] = kwargs[field]
                
        return request.render('tp_vendor_registration.vendor_registration_form', values)
    
    @http.route(['/vendor-registration/submit'], type='http', auth="public", 
                website=True, methods=['POST'], csrf=False)
    def vendor_registration_submit(self, **post):
        """Process vendor registration form submission"""
        # Initialize error tracking
        error = {}
        error_message = []
        
        # Get countries for re-rendering form if needed
        countries = request.env['res.country'].sudo().search([])
        
        # Required field validation
        required_fields = {
            'name': 'Contact Person',
            'email': 'Email Address', 
            'company_name': 'Company Name'
        }
        
        for field, label in required_fields.items():
            if not post.get(field, '').strip():
                error[field] = 'missing'
                error_message.append(f'{label} is required.')
        
        # Email validation
        email = post.get('email', '').strip()
        if email and not self._validate_email(email):
            error['email'] = 'invalid'
            error_message.append('Please enter a valid email address.')
        elif not email:
            error['email'] = 'missing'
            if 'Email Address is required.' not in error_message:
                error_message.append('Email Address is required.')
        
        # If there are validation errors, redisplay form
        if error_message:
            values = {
                'countries': countries,
                'error': error,
                'error_message': error_message,
                'name': post.get('name', ''),
                'email': post.get('email', ''),
                'phone': post.get('phone', ''),
                'company_name': post.get('company_name', ''),
                'street': post.get('street', ''),
                'city': post.get('city', ''),
                'zip_code': '',  # Keep empty as requested
                'website': '',   # Keep empty as requested
                'tax_id': post.get('tax_id', ''),
                'department': post.get('department', ''),
                'department_notes': post.get('department_notes', ''),
                'business_type': post.get('business_type', 'company'),
                'country_id': post.get('country_id', ''),
            }
            return request.render('tp_vendor_registration.vendor_registration_form', values)
        
        # Create vendor request
        try:
            vendor_request_vals = {
                'name': post.get('name', '').strip(),
                'email': post.get('email', '').strip(),
                'phone': post.get('phone', '').strip(),
                'company_name': post.get('company_name', '').strip(),
                'street': post.get('street', '').strip(),
                'city': post.get('city', '').strip(),
                'zip': post.get('zip', '').strip(),
                'country_id': int(post.get('country_id')) if post.get('country_id') and post.get('country_id').isdigit() else False,
                'website': post.get('website', '').strip(),
                'tax_id': post.get('tax_id', '').strip(),
                'department': post.get('department', ''),
                'department_notes': post.get('department_notes', '').strip(),
                'business_type': post.get('business_type', 'company'),
                'status': 'submitted',
            }
            
            vendor_request = request.env['vendor.request'].sudo().create(vendor_request_vals)
            
            _logger.info(f'Vendor registration submitted: {vendor_request.company_name} - ID: {vendor_request.id}')
            
            return request.render('tp_vendor_registration.vendor_registration_thanks', {
                'vendor_request': vendor_request
            })
            
        except Exception as e:
            _logger.error(f'Error creating vendor request: {str(e)}')
            
            # Return form with error message
            values = {
                'countries': countries,
                'error': {},
                'error_message': ['An unexpected error occurred. Please try again or contact support.'],
                'name': post.get('name', ''),
                'email': post.get('email', ''),
                'phone': post.get('phone', ''),
                'company_name': post.get('company_name', ''),
                'street': post.get('street', ''),
                'city': post.get('city', ''),
                'zip_code': '',
                'website': '', 
                'tax_id': post.get('tax_id', ''),
                'department': post.get('department', ''),
                'department_notes': post.get('department_notes', ''),
                'business_type': post.get('business_type', 'company'),
                'country_id': post.get('country_id', ''),
            }
            return request.render('tp_vendor_registration.vendor_registration_form', values)