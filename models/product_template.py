from odoo import models,fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'


    def action_do_somthing(self):
        print(self,'inside action_do_somthing method')