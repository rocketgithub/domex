# -*- coding: utf-8 -*-

from odoo import api, models
import re
import datetime
from datetime import date
import logging
# import odoo.addons.l10n_gt_extra.a_letras

class ReportContraseniaPago(models.AbstractModel):
    _name = 'report.domex.contrasenia_pago'

    def fecha_impresion(self):
        fecha = str(datetime.datetime.strptime(str(date.today()), '%Y-%m-%d').date())
        return fecha

    def _get_facturas(self,facturas):
        logging.warn(facturas)
        factura_dic = {}
        for factura in facturas:
            if factura.partner_id.id not in factura_dic:
                factura_dic.update({factura.partner_id.id: {'compras': [],'facturas':[],'nombre': factura.partner_id.name, 'total':0}   })
            factura_dic[factura.partner_id.id]['total'] += factura.amount_total
            factura_dic[factura.partner_id.id]['compras'].append(factura.origin)
            factura_dic[factura.partner_id.id]['facturas'].append(factura)
                # factura_dic[factura.id]['compra'] = factura.origin
                # factura_dic[factura.id]['proveedor'] = factura.partner_id.name
        logging.warn(factura_dic)
        primer_proveedor = next(iter(factura_dic))
        # logging.warn(primer_proveedor)
        factura_dic = factura_dic[primer_proveedor]
        factura_dic['compras'] = ','.join(factura_dic['compras'])
        logging.warn(factura_dic)
        return factura_dic

    @api.model
    def render_html(self, docids, data=None):
        self.model = 'account.invoice'
        docs = self.env[self.model].browse(docids)

        docargs = {
            'doc_ids': docids,
            'doc_model': self.model,
            'docs': docs,
            'fecha_impresion': self.fecha_impresion,
            '_get_facturas': self._get_facturas,
        }
        return self.env['report'].render('domex.contrasenia_pago', docargs)
