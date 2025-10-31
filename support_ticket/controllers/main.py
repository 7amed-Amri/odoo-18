from odoo import http
from odoo.http import request

class SupportTicketController(http.Controller):

    @http.route('/help', type='http', auth="public", website=True)
    def help_page(self, **kw):
        return request.render('support_ticket.help_page')

    @http.route('/help/submit', type='http', auth="public", website=True, csrf=False)
    def submit_ticket(self, **post):
        Ticket = request.env['support.ticket']
        Ticket.sudo().create({
            'name': post.get('subject'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'description': post.get('description'),
            'status': 'submitted'
        })
        return request.render('support_ticket.thank_you_page')
