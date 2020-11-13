# -*- coding: utf-8 -*-

from odoo import api, models
import re
import datetime
from datetime import date
import logging
# import odoo.addons.l10n_gt_extra.a_letras

class ReportContraseniasPago(models.AbstractModel):
    _name = 'report.domex.contrasenias_pago'

    def fecha_impresion(self):
        fecha = str(datetime.datetime.strptime(str(date.today()), '%Y-%m-%d').date())
        return fecha

    def _get_facturas(self,facturas):
        factura_dic = {}
        for factura in facturas:
            if factura.partner_id.id not in factura_dic:
                serie = ''
                numero = ''
                if factura.reference:
                    split = factura.reference.split('-')
                    if len(split) > 0:
                        serie = split[0]
                    if len(split) > 1:
                        numero = split[1]
                factura_dic.update({factura.partner_id.id: {'compras': [],'facturas':[],'nombre': factura.partner_id.name, 'nit': factura.partner_id.vat, 'serie': serie, 'numero': numero, 'total':0}   })       
            factura_dic[factura.partner_id.id]['total'] += factura.amount_total
            factura_dic[factura.partner_id.id]['compras'].append(factura.origin)
            factura_dic[factura.partner_id.id]['facturas'].append(factura)
        primer_proveedor = next(iter(factura_dic))
        factura_dic = factura_dic[primer_proveedor]
        factura_dic['compras'] = (','.join(factura_dic['compras'])) if factura_dic['compras'][0] != False else ''
        return factura_dic
    

    @api.model
    def render_html(self, docids, data=None):
        data = data if data is not None else {}
        self.model = 'account.invoice'
        docs = self.env[self.model].browse(data.get('ids', data.get('active_ids')))
        company_id = self.env['res.company'].search([('id','=', data['form']['company_id'][0])])
        docargs = {
            'doc_ids': data.get('ids', data.get('active_ids')),
            'doc_model': self.model,
            'docs': docs,
            'fecha_impresion': self.fecha_impresion,
            '_get_facturas': self._get_facturas,
            'company': company_id,
            'data': dict(
                data
            ),
        }
        return self.env['report'].render('domex.contrasenias_pago', docargs)
    