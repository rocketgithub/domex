# -*- coding: utf-8 -*-

from odoo import api, models
import odoo.addons.l10n_gt_extra.a_letras

class ReportAbstractVoucher(models.AbstractModel):
    _name = 'domex.abstract.reporte_voucher'

    nombre_reporte = ''

    def totales(self, o):
        t = {'debito': 0, 'credito': 0}
        for l in o.move_line_ids:
            t['debito'] += l.debit
            t['credito'] += l.credit
        return t

    @api.model
    def render_html(self, docids, data=None):
        self.model = 'account.payment'
        docs = self.env[self.model].browse(docids)

        docargs = {
            'doc_ids': docids,
            'doc_model': self.model,
            'docs': docs,
            'a_letras': odoo.addons.l10n_gt_extra.a_letras,
            'totales': self.totales,
        }
        return self.env['report'].render(self.nombre_reporte, docargs)

class ReportVoucher1(models.AbstractModel):
    _name = 'report.domex.reporte_voucher1'
    _inherit = 'domex.abstract.reporte_voucher'

    nombre_reporte = 'domex.reporte_voucher1'

class ReportVoucher2(models.AbstractModel):
    _name = 'report.domex.reporte_voucher2'
    _inherit = 'domex.abstract.reporte_voucher'

    nombre_reporte = 'domex.reporte_voucher2'

class ReportVoucher3(models.AbstractModel):
    _name = 'report.domex.reporte_voucher3'
    _inherit = 'domex.abstract.reporte_voucher'

    nombre_reporte = 'domex.reporte_voucher3'

class ReportVoucher4(models.AbstractModel):
    _name = 'report.domex.reporte_voucher4'
    _inherit = 'domex.abstract.reporte_voucher'

    nombre_reporte = 'domex.reporte_voucher4'

class ReportVoucher5(models.AbstractModel):
    _name = 'report.domex.reporte_voucher5'
    _inherit = 'domex.abstract.reporte_voucher'

    nombre_reporte = 'domex.reporte_voucher5'

class ReportVoucher6(models.AbstractModel):
    _name = 'report.domex.reporte_voucher6'
    _inherit = 'domex.abstract.reporte_voucher'

    nombre_reporte = 'domex.reporte_voucher6'

class ReportVoucher7(models.AbstractModel):
    _name = 'report.domex.reporte_voucher7'
    _inherit = 'domex.abstract.reporte_voucher'

    nombre_reporte = 'domex.reporte_voucher7'

class ReportVoucher8(models.AbstractModel):
    _name = 'report.domex.reporte_voucher8'
    _inherit = 'domex.abstract.reporte_voucher'

    nombre_reporte = 'domex.reporte_voucher8'
