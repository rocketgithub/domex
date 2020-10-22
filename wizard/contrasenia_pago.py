# -*- encoding: utf-8 -*-
from odoo import api, fields, models
import logging


class WizardContraseniaPago(models.TransientModel):
    _name = "domex.wizard_contrasenia"

    company_id = fields.Many2one('res.company', string='Compañía', required=True)

    @api.multi
    def action_report(self):
        datas={'ids': self.env.context.get('active_ids', [])}
        res = self.read(['company_id'])
        res = res and res[0] or {}
        datas['form'] = res
        return self.env['report'].get_action([], 'domex.contrasenias_pago', data=datas)