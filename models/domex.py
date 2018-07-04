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
                m.quantity_done = m.product_uom_qty * production.multiplicador_materia - m.product_uom_qty
                # m.product_qty = m.product_qty * production.multiplicador_materia
                # m.product_uom_qty = m.product_uom_qty * production.multiplicador_materia
                # m.ordered_qty = m.ordered_qty * production.multiplicador_materia
        return True

class SaleOrder(models.Model):
    _inherit = "sale.order"

    proyecto = fields.Char('Proyecto')
    atencion = fields.Char('Atención')
    supplier = fields.Many2one('res.partner', string='Supplier')
    bill_to = fields.Many2one('res.partner', string='Bill to')
    consigned_to = fields.Many2one('res.partner', string='Consigned to')
    send_docs_to = fields.Many2one('res.partner', string='Send Docs to')
    marks = fields.Text(string="Marks")
    insurance = fields.Char('Insurance')
    delivery = fields.Char('Delivery')
    comision = fields.Float('Comision de ventas')
    lugar_entrega = fields.Char('Lugar de entrega')
    tiempo_estimado_entrega = fields.Char('Tiempo estimado de entrega')

    @api.multi
    def recalcular_totales(self):
        for order in self:
            for line in order.order_line:
                line.price_unit = line.price_unit * line.largo
        return True