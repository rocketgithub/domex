# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp
import logging

class ProductTemplate(models.Model):
    _inherit = "product.template"

    costo_por_metro = fields.Float('Costo por metro', digits=dp.get_precision('Product Price'))

