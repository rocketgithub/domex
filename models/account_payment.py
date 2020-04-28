# -*- encoding: utf-8 -*-

from openerp import models, fields, api, _

class account_payment(models.Model):
    _inherit = 'account.payment'

    cuenta_transitoria_id = fields.Many2one('account.account', 'Cuenta transitoria')

    @api.one
    @api.depends('invoice_ids', 'payment_type', 'partner_type', 'partner_id')
    def _compute_destination_account_id(self):
        super(account_payment, self)._compute_destination_account_id()
        if self.cuenta_transitoria_id:
            self.destination_account_id = self.cuenta_transitoria_id.id
