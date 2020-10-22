# -*- coding: utf-8 -*-

from odoo import api, models
import re
import datetime
from datetime import date
import logging
# import odoo.addons.l10n_gt_extra.a_letras

class ReportPurchaseOrder(models.AbstractModel):
    _name = 'report.domex.purchase_orders'

    def fecha_impresion(self):
        fecha = str(datetime.datetime.strptime(str(date.today()), '%Y-%m-%d').date())
        return fecha
    
    @api.model
    def render_html(self, docids, data=None):
        data = data if data is not None else {}
        self.model = 'purchase.order'
        docs = self.env[self.model].browse(data.get('ids', data.get('active_ids')))
        company_id = self.env['res.company'].search([('id','=', data['form']['company_id'][0])])
        logging.warn(docs)
        docargs = {
            'doc_ids': data.get('ids', data.get('active_ids')),
            'doc_model': self.model,
            'docs': docs,
            'fecha_impresion': self.fecha_impresion,
            'company': company_id,
            'data': dict(
                data
            ),
        }
        return self.env['report'].render('domex.purchase_orders', docargs)
    