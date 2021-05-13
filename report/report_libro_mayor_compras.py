# -*- coding: utf-8 -*-

import datetime
import time
from datetime import date
from odoo import api, models, _
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
import logging
# import odoo.addons.l10n_gt_extra.a_letras

class LibroMayorCompras(models.AbstractModel):
    _name = 'report.domex.libro_mayor_compras'
    
    def _get_data(self, accounts, date_from, date_to, partner_id):
        moves_lines = dict(map(lambda x: (x, []), accounts.ids))
        
        for account in moves_lines:
            tipo = {}
            tipo['local'] = []
            tipo['exterior'] = []
            moves_lines[account].append(tipo)

        domain = []
        domain.append(('account_id.id', 'in', accounts.ids))
        if date_from:
            domain.append(('date', '>=', date_from))
        if date_to:
            domain.append(('date', '<=', date_to))
        if partner_id:
            domain.append(('partner_id.id', '<=', partner_id))
        MoveLines = self.env['account.move.line'].search(domain) 
        for row in MoveLines:
            balance = 0
            invoice = ""
            tipo_gasto = ""
            if row.invoice_id:
                invoice = row.invoice_id.name
                tipo_gasto = row.invoice_id.tipo_gasto
                
            ln = {}
            ln = {'lid': row.id, 'lname': row.name, 'partner_name': row.partner_id.name, 'debit': row.debit, 'move_name': row.move_id.name, 'currency_id': row.currency_id, 'credit': row.credit, 'lref': row.ref, 'amount_currency': row.amount_currency, 'balance': row.debit - row.credit, 'total_balance': 0, 'ldate': row.date, 'date_due': row.date_maturity, 'tipo_gasto': tipo_gasto}
                   
            if tipo_gasto == 'importacion':
                moves_lines[row.account_id.id][0]['exterior'].append(ln)
            else:
                moves_lines[row.account_id.id][0]['local'].append(ln)
            
            
            for line in moves_lines[row.account_id.id][0]['exterior']:
                balance += line['balance']
                line['total_balance'] += balance
                
            for line in moves_lines[row.account_id.id][0]['local']:
                balance += line['balance']
                line['total_balance'] += balance
                
            
        account_res = []
        for account in accounts:
            res = dict((fn, 0.0) for fn in ['credit', 'debit', 'balance', 'local_credit', 'local_debit', 'local_balance', 'exterior_credit', 'exterior_debit', 'exterior_balance'])
            res['code'] = account.code
            res['name'] = account.name
            res['local_move_lines'] = moves_lines[account.id][0]['local']
            res['exterior_move_lines'] = moves_lines[account.id][0]['exterior']
            res['currency_id'] = account.currency_id
            for line in res.get('local_move_lines'):
                res['local_debit'] += line['debit']
                res['local_credit'] += line['credit']
                res['local_balance'] = line['total_balance']
            for line in res.get('exterior_move_lines'):
                res['exterior_debit'] += line['debit']
                res['exterior_credit'] += line['credit']
                res['exterior_balance'] = line['total_balance']
            account_res.append(res)
        return account_res
   
    @api.model
    def render_html(self, docids, data=None):
        if not data.get('form') or not self.env.context.get('active_model'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_ids', []))
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        partner_id = data['form']['partner_id']
        accounts = self.env['account.account'].search([('id', 'in', data['form']['account_ids'])])
        accounts_res = self._get_data(accounts, date_from, date_to, partner_id)
        docargs = {
            'doc_ids': docids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'Accounts': accounts_res,
        }
        return self.env['report'].render('domex.libro_mayor_compras', docargs)