# -*- encoding: utf-8 -*-
from odoo import api, fields, models
import logging


class WizardCuentasPagarCobrar(models.TransientModel):
    _inherit = "account.common.partner.report"
    _name = "domex.wizard_cuentas_cobrar_pagar"

    amount_currency = fields.Boolean("With Currency", help="It adds the currency column on report if the currency differs from the company currency.")
    reconciled = fields.Boolean('Reconciled Entries')
    compania_id = fields.Many2one('res.company', string='Compañía', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner')

    def _print_report(self, data):
        data = self.pre_print_report(data)
        data['form'].update({'reconciled': self.reconciled, 'amount_currency': self.amount_currency, 'compania_id': self.compania_id.name, 'partner_id': self.partner_id.id})
        return self.env['report'].get_action(self, 'domex.cuentas_pagar_cobrar', data=data)