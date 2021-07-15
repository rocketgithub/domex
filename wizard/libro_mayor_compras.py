# -*- encoding: utf-8 -*-
from odoo import api, fields, models
import logging


class WizardLibroMayorCompras(models.TransientModel):
    _inherit = "account.common.account.report"
    _name = "domex.wizard_libro_mayor_compras"

    local_account_ids = fields.Many2many("account.account",'model_local_rel', string="Cuenta para Compras Locales", required=True, default=False)
    exterior_account_ids = fields.Many2many("account.account", 'model_exterior_rel', string="Cuenta para Compras Exterior", required=True, default=False)
    compania_id = fields.Many2one('res.company', string='Compañía', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner')

    def _print_report(self, data):
        data = self.pre_print_report(data)
        data['form'].update({'compania_id': self.compania_id.name, 'local_account_ids': self.local_account_ids.ids, 'exterior_account_ids': self.exterior_account_ids.ids, 'partner_id': self.partner_id.id})
        records = self.env[data['model']].browse(data.get('ids', []))
        return self.env['report'].with_context(landscape=True).get_action(records, 'domex.libro_mayor_compras', data=data) 