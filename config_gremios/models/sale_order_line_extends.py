from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    filtered_product_id = fields.Many2one(
        comodel_name='product.template',
        string="Filtered Product",
        #domain="[('id', 'in', applicable_product_ids.ids)]"
    )
    select_list = fields.Selection(
        selection='_get_selection_list',
        string='Selection Field',
    )

   
    
    applicable_product_ids = fields.Many2many(
        comodel_name='product.template',
        compute='_compute_applicable_products',
        store=False,
        string="Applicable Products"
    )

    def _get_selection_list(self):
        """
        Método para generar dinámicamente las opciones del campo Selection.
        Devuelve una lista de tuplas [(id como string, nombre del producto)].
        """
        if self.applicable_product_ids:
             selection = [(str(product.id), product.name) for product in self.applicable_product_ids]
        # Aquí puedes filtrar los productos en base a tus condicionese
        else:
            products = self.env['product.template'].search([('sale_ok', '=', True)])
        # Generar la lista de tuplas (id como string, nombre)
        selection = [(str(product.id), product.name) for product in products]
        return selection

    @api.depends('order_id.pricelist_id', 'order_id.studio_almacen')
    def _compute_applicable_products(self):
        _logger.warning(f"Entrando en _compute_applicable_products")
        for line in self:
            pricelist = line.order_id.pricelist_id
            warehouse = line.order_id.studio_almacen
            _logger.warning(f"Pricelist: {pricelist}")
            _logger.warning(f"Warehouse: {warehouse}")

            products = self.env['product.template'].search([
                        ('sale_ok', '=', True),
                    ])
            if pricelist and warehouse:
                if pricelist.id != 1:
                    _logger.warning(f"no es la lista por defecto ")
                    # Obtener reglas de precios para la lista de precios seleccionada
                    pricelist_items = self.env['product.pricelist.item'].search([
                        ('pricelist_id', '=', pricelist.id),
                    ])

                    
                    
                    _logger.warning(f"pricelist_items: {pricelist_items} ")

                    #for item in pricelist_items:
                    #    _logger.warning(f"item: {item} - producto {item.product_id} producto {item.product_tmpl_id}")
                        
                    
                    #product_template_ids =[item.product_tmpl_id.id for item in pricelist_items]
                    product_ids = pricelist_items.mapped('product_tmpl_id.id')

                    #for producto in product_ids:
                    #    _logger.warning(f"product.template: {producto.product_variant_id}")
                    #product_product_ids=self.env['product.template'].search([
                    #    ('product_tmpl_id', 'in', product_ids),
                    #])

                    _logger.warning(f"product_ids: {product_ids}")

                    products=product_ids
                    """
                    # Filtrar productos disponibles en el almacén
                    products = self.env['product.template'].search([
                        ('id', 'in', product_product_ids.ids),
                        ('sale_ok', '=', True),
                        ('qty_available', '>', 0),
                        ('product_tmpl_id.product_variant_ids.stock_quant_ids.location_id', '=', warehouse.lot_stock_id.id)
                    ])

                    """

                    _logger.warning(f"products: {products} \ntipo de los products{type(products)}")
                
                line.applicable_product_ids = products
                _logger.warning(f"productos con el browse {self.env['product.template'].browse(products)}")
                    #line.filtered_product_id = self.env['product.template'].browse(products)  
    @api.depends('order_id.pricelist_id', 'order_id.studio_almacen')
    def _compute_applicable_products(self):
        _logger.warning("Entrando en _compute_applicable_products")
        for line in self:
            pricelist = line.order_id.pricelist_id
            warehouse = line.order_id.studio_almacen
            applicable_products = self.env['product.template']
    
            _logger.warning(f"Pricelist: {pricelist}, Warehouse: {warehouse}")
    
            if pricelist:
                # Obtener reglas de precios para la lista seleccionada
                pricelist_items = self.env['product.pricelist.item'].search([
                    ('pricelist_id', '=', pricelist.id),
                    ('product_tmpl_id', '!=', False)  # Asegurarse de que haya plantillas de productos
                ])
                _logger.warning(f"pricelist_items: {pricelist_items}")
    
                product_template_ids = pricelist_items.mapped('product_tmpl_id.id')
                _logger.warning(f"product_template_ids: {product_template_ids}")
    
                if product_template_ids:
                    applicable_products = self.env['product.template'].browse(product_template_ids)
    
            _logger.warning(f"Final applicable products: {applicable_products}")
            line.applicable_product_ids = applicable_products


    @api.onchange('filtered_product_id')
    def _onchange_filtered_product_id(self):
        """Cuando el usuario selecciona un producto filtrado, asignarlo a product_id."""
        if self.filtered_product_id:
            # Selecciona automáticamente el producto base
            product_variant = self.filtered_product_id.product_variant_id
            if product_variant:
                self.product_id = product_variant








