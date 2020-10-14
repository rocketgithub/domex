# -*- coding: utf-8 -*-

from odoo import api, models
import odoo.addons.l10n_gt_extra.a_letras

class ReportAbstractVoucher(models.AbstractModel):
    _name = 'domex.abstract.reporte_voucher'

    nombre_reporte = ''

    def anio(self, o):
        partes = o.payment_date.split('-')
        if len(partes) > 0:
            return partes[0]
        else:
            return ''

    def mes(self, o):
        partes = o.payment_date.split('-')
        if len(partes) > 1:
            return partes[1]
        else:
            return ''

    def dia(self, o):
        partes = o.payment_date.split('-')
        if len(partes) > 2:
            return partes[2]
        else:
            return ''

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
            'anio': self.anio,
            'dia': self.dia,
            'mes': self.mes,
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

class ReportVoucher9(models.AbstractModel):
    _name = 'report.domex.reporte_voucher9'
    _inherit = 'domex.abstract.reporte_voucher'

    nombre_reporte = 'domex.reporte_voucher9'

class ReportVoucher10(models.AbstractModel):
    _name = 'report.domex.reporte_voucher10'
    _inherit = 'domex.abstract.reporte_voucher'

    nombre_reporte = 'domex.reporte_voucher10'

class ReportVoucher11(models.AbstractModel):
    _name = 'report.domex.reporte_voucher11'
    _inherit = 'domex.abstract.reporte_voucher'

    nombre_reporte = 'domex.reporte_voucher11'

class ReportVoucher12(models.AbstractModel):
    _name = 'report.domex.reporte_voucher12'
    _inherit = 'domex.abstract.reporte_voucher'

    nombre_reporte = 'domex.reporte_voucher12'

class ReportVoucher13(models.AbstractModel):
    _name = 'report.domex.reporte_voucher13'
    _inherit = 'domex.abstract.reporte_voucher'

    nombre_reporte = 'domex.reporte_voucher13'

class ReportVoucher14(models.AbstractModel):
    _name = 'report.domex.reporte_voucher14'
    _inherit = 'domex.abstract.reporte_voucher'

    nombre_reporte = 'domex.reporte_voucher14'

class ReportVoucher15(models.AbstractModel):
    _name = 'report.domex.reporte_voucher15'
    _inherit = 'domex.abstract.reporte_voucher'

    nombre_reporte = 'domex.reporte_voucher15'

class ReportVoucher16(models.AbstractModel):
    _name = 'report.domex.reporte_voucher16'
    _inherit = 'domex.abstract.reporte_voucher'

    nombre_reporte = 'domex.reporte_voucher16'

class ReportVoucher17(models.AbstractModel):
    _name = 'report.domex.reporte_voucher17'
    _inherit = 'domex.abstract.reporte_voucher'

    nombre_reporte = 'domex.reporte_voucher17'

class ReportVoucher18(models.AbstractModel):
    _name = 'report.domex.reporte_voucher18'
    _inherit = 'domex.abstract.reporte_voucher'

    nombre_reporte = 'domex.reporte_voucher18'

class ReportVoucher19(models.AbstractModel):
    _name = 'report.domex.reporte_voucher19'
    _inherit = 'domex.abstract.reporte_voucher'

    nombre_reporte = 'domex.reporte_voucher19'

class ReportVoucher20(models.AbstractModel):
    _name = 'report.domex.reporte_voucher20'
    _inherit = 'domex.abstract.reporte_voucher'

    nombre_reporte = 'domex.reporte_voucher20'

class ReportVoucher21(models.AbstractModel):
    _name = 'report.domex.reporte_voucher21'
    _inherit = 'domex.abstract.reporte_voucher'

    nombre_reporte = 'domex.reporte_voucher21'

class ReportVoucher22(models.AbstractModel):
    _name = 'report.domex.reporte_voucher22'
    _inherit = 'domex.abstract.reporte_voucher'

    nombre_reporte = 'domex.reporte_voucher22'

class ReportVoucher23(models.AbstractModel):
    _name = 'report.domex.reporte_voucher23'
    _inherit = 'domex.abstract.reporte_voucher'

    nombre_reporte = 'domex.reporte_voucher23'
