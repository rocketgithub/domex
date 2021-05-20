from odoo import models, fields, api
import logging


class Quant(models.Model):
    _inherit = "stock.quant"
    
    @api.one
    @api.depends('largo','qty')
    def _cantidad_en_metros(self):
        if self.largo:
            self.cantidad_en_metros = self.largo * self.qty
        else:
            self.cantidad_en_metros = 0

    @api.one
    @api.depends('product_id','cantidad_en_metros')
    def _costo_total_en_metros(self):
        if self.cantidad_en_metros != 0:
            self.costo_total_en_metros = self.product_id.costo_por_metro * self.cantidad_en_metros
        else:
            self.costo_total_en_metros = 0
        
    largo = fields.Float(related='lot_id.largo', store=True, readonly=True)
    cantidad_en_metros = fields.Float('Cantidad en metros', compute='_cantidad_en_metros')
    costo_total_en_metros = fields.Float('Costo total en metros', compute='_costo_total_en_metros')