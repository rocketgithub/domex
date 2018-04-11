# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Color(models.Model):
    _name = 'domex.color'

    name = fields.Char("Nombre")

class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    largo = fields.Float('Largo')
    ancho = fields.Float('Ancho')
    color_id = fields.Many2one('domex.color', string='Color')
    calibre = fields.Float('Calibre')
    aislante = fields.Char('Aislante')
    cantidad_planchas = fields.Integer('Cantidad de planchas')

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    largo = fields.Float('Largo')
    ancho = fields.Float('Ancho')
    color_id = fields.Many2one('domex.color', string='Color')
    calibre = fields.Float('Calibre')
    aislante = fields.Char('Aislante')
    cantidad_planchas = fields.Integer('Cantidad de planchas')

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    multiplicador_materia = fields.Float('Multiplicador materia')

    @api.multi
    def multiplicar(self):
        for production in self:
            for m in production.move_raw_ids:
                m.product_uom_qty = m.product_uom_qty * production.multiplicador_materia
        return True
