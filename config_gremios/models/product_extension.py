from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_in_pricelist = fields.Boolean(
        compute='_compute_is_in_pricelist',
        store=False
    )

    def _compute_is_in_pricelist(self):
        _logger.warning(f"Entrando a _compute_is_in_pricelist")
        _logger.warning(f"contexto: {self.env.context}")
        active_pricelist = self.env.context.get('active_pricelist_id')
        if active_pricelist:
            pricelist_items = self.env['product.pricelist.item'].search([
                ('pricelist_id', '=', active_pricelist),
                ('product_id', '!=', False)
            ])
            applicable_ids = pricelist_items.mapped('product_id.id')
            for product in self:
                product.is_in_pricelist = product.id in applicable_ids
        else:
            for product in self:
                product.is_in_pricelist = False
