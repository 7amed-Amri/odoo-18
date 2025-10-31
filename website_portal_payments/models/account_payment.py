# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def name_get(self):
        if self.env.user.has_group('base.group_portal'):
            return super(AccountPayment, self.sudo()).name_get()
        else:
            return super(AccountPayment, self).name_get()

    def _compute_access_url(self):
        super(AccountPayment, self)._compute_access_url()
        for rec in self:
            rec.access_url = '/custom_payment/printpayment/%s' % (rec.id)

    def _get_report_base_filename(self):
        """Filename used by portal _show_report"""
        self.ensure_one()
        return _('Payment Receipt - %s') % (self.name or self.ref or '')