# -*- encoding: utf-8 -*-
from odoo import api, fields, models
import logging


class WizardLibroMayorCompras(models.TransientModel):
    _inherit = "account.common.account.report"
    _name = "domex.wizard_libro_mayor_compras"

    account_ids = fields.Many2many("account.account", string="Cuenta", required=True, default=False)
    compania_id = fields.Many2one('res.company', string='Compañía', required=True)

    def _print_report(self, data):
        data = self.pre_print_report(data)
        data['form'].update({'compania_id': self.compania_id.name, 'account_ids': self.account_ids.ids})
        records = self.env[data['model']].browse(data.get('ids', []))
        return self.env['report'].with_context(landscape=True).get_action(records, 'domex.libro_mayor_compras', data=data) 