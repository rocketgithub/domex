# -*- coding: utf-8 -*-

import datetime
import time
from datetime import date
from odoo import api, models, _
from odoo.exceptions import UserError
import logging

class LibroMayorCompras(models.AbstractModel):
    _name = 'report.domex.libro_mayor_compras'
    
    def _get_data(self, local_accounts, exterior_accounts, date_from, date_to, partner_id):
        move_lines = {}
        move_lines['local'] = dict(map(lambda x: (x, []), local_accounts.ids))
        move_lines['exterior'] = dict(map(lambda x: (x, []), exterior_accounts.ids))
        domain_l = [('account_id.id', 'in', local_accounts.ids)]
        domain_e = [('account_id.id', 'in', exterior_accounts.ids)]
        if date_from:
            domain_l.append(('date', '>=', date_from))
            domain_e.append(('date', '>=', date_from))
        if date_to:
            domain_l.append(('date', '<=', date_to))
            domain_e.append(('date', '<=', date_to))
        if partner_id:
            domain_l.append(('partner_id.id', '<=', partner_id))
            domain_e.append(('partner_id.id', '<=', partner_id))
        MoveLines_locales = self.env['account.move.line'].search(domain_l)
        MoveLines_exterior = self.env['account.move.line'].search(domain_e)
        
        for row in MoveLines_locales:
            balance = 0
            ln = {}
            ln = {'lid': row.id, 'lname': row.name, 'partner_name': row.partner_id.name, 'debit': row.debit, 'move_name': row.move_id.name, 'currency_id': row.currency_id, 'credit': row.credit, 'lref': row.ref, 'amount_currency': row.amount_currency, 'balance': row.debit - row.credit, 'total_balance': 0, 'ldate': row.date, 'date_due': row.date_maturity}
            move_lines['local'][row.account_id.id].append(ln)
            for line in move_lines['local'][row.account_id.id]:
                balance += line['balance']
                line['total_balance'] += balance
                    
        for row in MoveLines_exterior:
            balance = 0
            ln = {}
            ln = {'lid': row.id, 'lname': row.name, 'partner_name': row.partner_id.name, 'debit': row.debit, 'move_name': row.move_id.name, 'currency_id': row.currency_id, 'credit': row.credit, 'lref': row.ref, 'amount_currency': row.amount_currency, 'balance': row.debit - row.credit, 'total_balance': 0, 'ldate': row.date, 'date_due': row.date_maturity}
            move_lines['exterior'][row.account_id.id].append(ln)
            for line in move_lines['exterior'][row.account_id.id]:
                balance += line['balance']
                line['total_balance'] += balance
                    
        account_res = [[], []]
        for account in local_accounts:
            res = dict((fn, 0.0) for fn in ['credit', 'debit', 'balance'])
            res['code'] = account.code
            res['name'] = account.name
            res['move_lines'] = move_lines['local'][account.id]
            res['currency_id'] = account.currency_id
            for line in res.get('move_lines'):
                res['debit'] += line['debit']
                res['credit'] += line['credit']
                res['balance'] = line['total_balance']
            account_res[0].append(res)
        for account in exterior_accounts:
            res = dict((fn, 0.0) for fn in ['credit', 'debit', 'balance'])
            res['code'] = account.code
            res['name'] = account.name
            res['move_lines'] = move_lines['exterior'][account.id]
            res['currency_id'] = account.currency_id
            for line in res.get('move_lines'):
                res['debit'] += line['debit']
                res['credit'] += line['credit']
                res['balance'] = line['total_balance']
            account_res[1].append(res)
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
        local_accounts = self.env['account.account'].search([('id', 'in', data['form']['local_account_ids'])])
        exterior_accounts = self.env['account.account'].search([('id', 'in', data['form']['exterior_account_ids'])])
        accounts_res = self._get_data(local_accounts, exterior_accounts, date_from, date_to, partner_id)
        docargs = {
            'doc_ids': docids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'Accounts': accounts_res,
        }
        return self.env['report'].render('domex.libro_mayor_compras', docargs)