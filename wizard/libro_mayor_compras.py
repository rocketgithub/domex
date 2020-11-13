# -*- encoding: utf-8 -*-
from odoo import api, fields, models
import logging


class WizardLibroMayorCompras(models.TransientModel):
    _inherit = "account.common.account.report"
    _name = "domex.wizard_libro_mayor_compras"

    journal_ids = fields.Many2many('account.journal', 'account_libro_mayor_rel', 'account_id', 'journal_id', string='Journals', required=True)
    compania_id = fields.Many2one('res.company', string='Compañía', required=True)

    def _print_report(self, data):
        data = self.pre_print_report(data)
        data['form'].update({'compania_id': self.compania_id.name})
        records = self.env[data['model']].browse(data.get('ids', []))
        return self.env['report'].with_context(landscape=True).get_action(records, 'domex.libro_mayor_compras', data=data) 