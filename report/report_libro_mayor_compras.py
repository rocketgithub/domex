# -*- coding: utf-8 -*-

import datetime
import time
from datetime import date
from odoo import api, models, _
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
import logging
# import odoo.addons.l10n_gt_extra.a_letras

class ReportGeneralLedger(models.AbstractModel):
    _inherit = "report.account.report_generalledger"
    _name = 'report.domex.libro_mayor_compras'
    
    def _get_account_move_entry(self, accounts, init_balance, sortby, display_account):
        account_res = super(ReportGeneralLedger, self)._get_account_move_entry(accounts, init_balance, sortby, display_account)
        for account in account_res:
            for line in account['move_lines']:
                partner_country = self.env['res.partner'].search([('name', '=', line['partner_name'])]).country_id.name
                if partner_country == 'Guatemala':
                    line.update({'compra': 'local'})
                else:
                    line.update({'compra': 'exterior'})
                    
                move_date_due = self.env['account.invoice'].search([('number', '=', line['move_name'])]).date_due
                line.update({'date_due': move_date_due})           
        return account_res
   
    @api.model
    def render_html(self, docids, data=None):
        if not data.get('form') or not self.env.context.get('active_model'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_ids', []))

        init_balance = False
        sortby = False
        display_account =  data['form']['display_account']
        codes = []
        if data['form'].get('journal_ids', False):
            codes = [journal.code for journal in self.env['account.journal'].search([('id', 'in', data['form']['journal_ids'])])]

        accounts = docs if self.model == 'account.account' else self.env['account.account'].search([])
        accounts_res = self.with_context(data['form'].get('used_context',{}))._get_account_move_entry(accounts, init_balance, sortby, display_account)
        docargs = {
            'doc_ids': docids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'Accounts': accounts_res,
            'print_journal': codes,
        }
        return self.env['report'].render('domex.libro_mayor_compras', docargs)