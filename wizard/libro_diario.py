# -*- encoding: utf-8 -*-
from odoo import api, fields, models
import logging


class WizardLibroDiario(models.TransientModel):
    _inherit = "l10n_gt_extra.asistente_reporte_diario"

    agrupado_por_partida = fields.Boolean(string="Agrupado por partida")
    
class ReporteDiario(models.AbstractModel):
    _inherit = 'report.l10n_gt_extra.reporte_diario'

    def lineas(self, datos):
        res = super(ReporteDiario, self).lineas(datos)
        if datos['agrupado_por_partida']:
            totales = {}
            lineas_resumidas = {}
            lineas=[]
            totales['debe'] = 0
            totales['haber'] = 0
            totales['saldo_inicial'] = 0
            totales['saldo_final'] = 0
            accounts_str = ','.join([str(x) for x in datos['cuentas_id']])
            
            self.env.cr.execute('select a.id, a.code as codigo, a.name as cuenta, l.date as fecha, l.move_id as partida, t.include_initial_balance as balance_inicial, sum(l.debit) as debe, sum(l.credit) as haber ' \
            	'from account_move_line l join account_account a on(l.account_id = a.id)' \
            	'join account_account_type t on (t.id = a.user_type_id)' \
            	'where a.id in ('+accounts_str+') and l.date >= %s and l.date <= %s group by a.id, a.code, a.name,l.date,l.move_id, t.include_initial_balance ORDER BY l.move_id,l.date,a.code',
            (datos['fecha_desde'], datos['fecha_hasta']))

            for r in self.env.cr.dictfetchall():
                totales['debe'] += r['debe']
                totales['haber'] += r['haber']
                linea = {
                    'id': r['id'],
                    'fecha': r['fecha'],
                    'partida': r['partida'],
                    'codigo': r['codigo'],
                    'cuenta': r['cuenta'],
                    'saldo_inicial': 0,
                    'debe': r['debe'],
                    'haber': r['haber'],
                    'saldo_final': 0,
                    'balance_inicial': r['balance_inicial']
                }
                lineas.append(linea)
                
            for l in lineas:
                if not l['balance_inicial']:
                    l['saldo_inicial'] += self.retornar_saldo_inicial_inicio_anio(l['id'], datos['fecha_desde'])
                    l['saldo_final'] += l['saldo_inicial'] + l['debe'] - l['haber']
                    totales['saldo_inicial'] += l['saldo_inicial']
                    totales['saldo_final'] += l['saldo_final']
                else:
                    l['saldo_inicial'] += self.retornar_saldo_inicial_todos_anios(l['id'], datos['fecha_desde'])
                    l['saldo_final'] += l['saldo_inicial'] + l['debe'] - l['haber']
                    totales['saldo_inicial'] += l['saldo_inicial']
                    totales['saldo_final'] += l['saldo_final']

            cuentas_agrupadas = {}
            llave = 'partida'
            for l in lineas:
                if l[llave] not in cuentas_agrupadas:
                    move = self.env['account.move'].search([('id','=',l[llave])])
                    cuentas_agrupadas[l[llave]] = {'partida': l[llave], 'move_name': move.name, 'ref': move.ref, 'fecha': l['fecha'], 'cuentas': [], 'total_debe': 0, 'total_haber': 0}
                cuentas_agrupadas[l[llave]]['cuentas'].append(l)

            for la in cuentas_agrupadas.values():
                for l in la['cuentas']:
                    la['total_debe'] += l['debe']
                    la['total_haber'] += l['haber']

            lineas = cuentas_agrupadas.values()
            res = {'lineas': lineas,'totales': totales }
        return res
            
    
    