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
    atencion = fields.Many2one('res.partner', string='Atención')
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
    medidas = fields.Char('Medidas')
    oferta_por = fields.Char("Oferta por") 
    no_incluyen = fields.Text("Precios no incluyen")
    incluyen = fields.Char("Precios incluyen")
    tiempo_instalacion = fields.Char("Tiempo de instalación")
    
    @api.multi
    def recalcular_totales(self):
        for order in self:
            for line in order.order_line:
                line.price_unit = line.price_unit * line.largo
        return True

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    supplier_order_ref = fields.Char(string='Referencia proveedor')
    bill_to = fields.Many2one('res.partner', string='Bill to')
    consigned_to = fields.Many2one('res.partner', string='Consigned to')
    send_docs_to = fields.Many2one('res.partner', string='Send Docs to')
    marks = fields.Text(string="Marks")
    insurance = fields.Char('Insurance')
    delivery = fields.Char('Delivery')
    proyecto = fields.Char('Proyecto')
    solicitante = fields.Many2one('res.partner', string='Solicitante')
    lugar_entrega = fields.Char('Lugar de entrega')

    
class StockPicking(models.Model):
    _inherit = "stock.picking"

    encargado_entrega = fields.Many2one('res.users', string='Encargado de la entrega')
    

class OrdenTrabajo(models.Model):
    _inherit = 'orden.trabajo'

    fecha_produccion = fields.Date('Fecha de Producción')
    observaciones = fields.Text(string="Observaciones")
    revisado_por = fields.Many2one('res.users', string='Revisado por')
    autorizado_por = fields.Many2one('res.users', string='Autorizado por')
    
    def obtener_cortes(self, cortes):
        medidas = []
        res = []
        
        for line in cortes:
            if line.corte1 not in medidas:
                medidas.append(line.corte1)
                res.append({'medida': line.corte1, 'cantidad': 0})
            for item in res:
                if item['medida'] == line.corte1:
                    item['cantidad'] += line.corte1 * line.product_qty
            
            if line.corte2 not in medidas:
                medidas.append(line.corte2)
                res.append({'medida': line.corte2, 'cantidad': 0})
            for item in res:
                if item['medida'] == line.corte2:
                    item['cantidad'] += line.corte2 * line.product_qty
                    
            if line.corte3 not in medidas:
                medidas.append(line.corte3)
                res.append({'medida': line.corte3, 'cantidad': 0})
            for item in res:
                if item['medida'] == line.corte3:
                    item['cantidad'] += line.corte3 * line.product_qty
            
            if line.corte4 not in medidas:
                medidas.append(line.corte4)
                res.append({'medida': line.corte4, 'cantidad': 0})
            for item in res:
                if item['medida'] == line.corte4:
                    item['cantidad'] += line.corte4 * line.product_qty
            
            if line.corte5 not in medidas:
                medidas.append(line.corte5)
                res.append({'medida': line.corte5, 'cantidad': 0})
            for item in res:
                if item['medida'] == line.corte5:
                    item['cantidad'] += line.corte5 * line.product_qty
            
            if line.corte6 not in medidas:
                medidas.append(line.corte6)
                res.append({'medida': line.corte6, 'cantidad': 0})
            for item in res:
                if item['medida'] == line.corte6:
                    item['cantidad'] += line.corte6 * line.product_qty
                    
            if line.sobra not in medidas:
                medidas.append(line.sobra)
                res.append({'medida': line.sobra, 'cantidad': 0})
            for item in res:
                if item['medida'] == line.sobra:
                    item['cantidad'] += line.sobra * line.product_qty            
        return res


class AccountMove(models.Model):
    _inherit = "account.move"

    tipo_gasto = fields.Selection([('compra', 'Compra/Bien'), ('servicio', 'Servicio'), ('importacion', 'Importación/Exportación'), ('combustible', 'Combustible'), ('mixto', 'Mixto')], string="Tipo de Gasto")
    
            
class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    tipo_gasto = fields.Selection([('compra', 'Compra/Bien'), ('servicio', 'Servicio'), ('importacion', 'Importación/Exportación'), ('combustible', 'Combustible'), ('mixto', 'Mixto')], string="Tipo de Gasto", related='move_id.tipo_gasto',store=True)
    