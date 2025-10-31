# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from collections import OrderedDict
from odoo.osv.expression import OR
from odoo.addons.portal.controllers.portal import CustomerPortal as website_account, pager as portal_pager

class website_account(website_account):
    
    def _prepare_portal_layout_values(self):
        values = super(website_account, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        payment = request.env['account.payment']
        payment_count = payment.sudo().search_count([
          ('partner_id', 'child_of', [partner.commercial_partner_id.id]),
          ('payment_type', 'in', ['inbound', 'outbound']),
          ('state','in',['draft', 'in_process', 'paid', 'canceled', 'rejected'])
          ])
        values.update({
            'custom_payment_count': payment_count,
        })
        return values

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id
        payment = request.env['account.payment']
        payment_count = payment.sudo().search_count([
          ('partner_id', 'child_of', [partner.commercial_partner_id.id]),
          ('payment_type', 'in', ['inbound', 'outbound']),
          ('state','in',['draft', 'in_process', 'paid', 'canceled', 'rejected'])
          ])
        values.update({
            'custom_payment_count': payment_count,
        })
        return values

    def _get_grouped_payments(self, payments, groupby):
        """Group payments by specified field"""
        if groupby == 'none':
            return [('', payments)]
        
        grouped_payments = OrderedDict()
        
        for payment in payments:
            if groupby == 'journal':
                group_key = payment.journal_id.name if payment.journal_id else _('No Journal')
            elif groupby == 'payment_method':
                group_key = payment.payment_method_line_id.name if payment.payment_method_line_id else _('No Payment Method')
            elif groupby == 'state':
                group_key = dict(payment._fields['state'].selection).get(payment.state, payment.state)
            else:
                group_key = _('Other')
            
            if group_key not in grouped_payments:
                grouped_payments[group_key] = request.env['account.payment']
            grouped_payments[group_key] |= payment
        
        return list(grouped_payments.items())

    # Payments
    @http.route(['/my/custom_payments', '/my/custom_payments/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_payments(self, page=1, sortby=None, filterby=None, search=None, search_in='content', groupby='none', **kw):
        values = self._prepare_portal_layout_values()
        
        partner = request.env.user.partner_id
        AccountPayment = request.env['account.payment']
        
        domain = [
            ('partner_id', 'child_of', [partner.commercial_partner_id.id]),
            ('payment_type', 'in', ['inbound', 'outbound']),
            ('state','in',['draft', 'in_process', 'paid', 'canceled', 'rejected'])
        ]
        
        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'journal': {'label': _('Journal'), 'order': 'journal_id desc'},
            'stage': {'label': _('Stage'), 'order': 'state'},
        }
        
        # Updated filters with new order
        searchbar_filters = OrderedDict([
            ('all', {'label': _('All'), 'domain': []}),
            ('customer', {'label': _('Customer Payments'), 'domain': [('payment_type','=','inbound')]}),
            ('vendor', {'label': _('Vendor Payments'), 'domain': [('payment_type','=','outbound')]}),
            ('draft', {'label': _('Draft'), 'domain': [('state','=','draft')]}),
            ('in_process', {'label': _('In Process'), 'domain': [('state','=','in_process')]}),
            ('paid', {'label': _('Paid'), 'domain': [('state','=','paid')]}),
            ('canceled', {'label': _('Canceled'), 'domain': [('state','=','canceled')]}),
            ('rejected', {'label': _('Rejected'), 'domain': [('state','=','rejected')]}),
        ])
        
        # Enhanced search inputs
        searchbar_inputs = {
            'content': {'input': 'content', 'label': _('Search in Ref. or Memo')},
            'memo': {'input': 'memo', 'label': _('Search in Memo')},
            'state': {'input': 'state', 'label': _('Search in State')},
            'journal': {'input': 'journal', 'label': _('Search in Journal')},
            'all': {'input': 'all', 'label': _('Search in All')},
        }
        
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'journal': {'input': 'journal', 'label': _('Journal')},
            'payment_method': {'input': 'payment_method', 'label': _('Payment Method')},
            'state': {'input': 'state', 'label': _('State')},
        }
        
        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']
        
        # Enhanced search functionality
        if search and search_in:
            if search_in == 'content':
                domain += ['|', ('name', 'ilike', search), ('memo', 'ilike', search)]
            elif search_in == 'memo':
                domain += [('memo', 'ilike', search)]
            elif search_in == 'state':
                domain += [('state', 'ilike', search)]
            elif search_in == 'journal':
                domain += [('journal_id.name', 'ilike', search)]
            elif search_in == 'all':
                domain += ['|', '|', '|', 
                          ('name', 'ilike', search), 
                          ('memo', 'ilike', search),
                          ('state', 'ilike', search),
                          ('journal_id.name', 'ilike', search)]

        # default group by value - Fixed groupby functionality
        if groupby == 'journal':
            order = "journal_id, %s" % order
        elif groupby == 'payment_method':
            order = "payment_method_line_id, %s" % order
        elif groupby == 'state':
            order = "state, %s" % order

        # count for pager
        payment_count = AccountPayment.sudo().search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/custom_payments",
            url_args={'groupby': groupby, 'sortby': sortby, 'filterby': filterby, 'search_in': search_in, 'search': search},
            total=payment_count, page=page, step=self._items_per_page
        )
        # content according to pager and archive selected
        payments = AccountPayment.sudo().search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        
        # Group payments if needed
        grouped_payments = self._get_grouped_payments(payments, groupby) if groupby != 'none' else None
        
        values.update({
            'payments': payments,
            'grouped_payments': grouped_payments,
            'page_name': 'payment',
            'pager': pager,
            'default_url': '/my/custom_payments',
            'searchbar_filters': searchbar_filters,
            'filterby': filterby,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_groupby': searchbar_groupby,
            'searchbar_inputs': searchbar_inputs,
            'search': search,
            'search_in': search_in,
            'sortby': sortby,
            'groupby': groupby,
        })
        return request.render("website_portal_payments.portal_my_payments", values)

    @http.route(['/custom_payment/printpayment/<model("account.payment"):payment>'], type='http', auth="user", website=True)
    def print_payment(self, payment, access_token=None, report_type='pdf', download=False, **kw):
        try:
            payment_sudo = self._document_check_access('account.payment', payment.id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=payment_sudo, report_type=report_type,
            report_ref='website_portal_payments.action_report_custom_payment_receipt',
            download=download)

        return request.redirect('/my')