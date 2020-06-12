# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def action_invoice_open(self):
        user = self.env['res.users'].browse(self.env.uid)
        if user.has_group('domex.facturas_usuario') == False:
            return super(AccountInvoice, self).action_invoice_open()
