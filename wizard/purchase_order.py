# -*- encoding: utf-8 -*-
from odoo import api, fields, models
import logging


class WizardPurchaseOrder(models.TransientModel):
    _name = "domex.wizard_po"

    company_id = fields.Many2one('res.company', string='Compañía', required=True)

    @api.multi
    def action_report(self):
        """Metodo que llama la lógica que genera el reporte"""
        datas={'ids': self.env.context.get('active_ids', [])}
        res = self.read(['company_id'])
        res = res and res[0] or {}
        datas['form'] = res
        return self.env['report'].get_action([], 'domex.purchase_orders', data=datas)