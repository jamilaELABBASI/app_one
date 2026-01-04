from odoo import models,fields


class SaleOrder(models.Model):
    # update existing model
    _inherit = 'sale.order'
    property_id=fields.Many2one('property')    # we add this relation to display all property in saleOrder form
    def action_confirm(self):
        res=super(SaleOrder,self).action_confirm()
        print('inside action_confirm method')
        return res
