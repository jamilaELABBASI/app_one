from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"
    property_id=fields.Many2one('property')

    # **** method 1 ****
    """
    # cette methode sera fonctionnelle si nous utilisons pas store cest a dire on veut juste afficher la valeure au niveau de la vue 
    price=fields.Float(compute='_compute_price')
    def _compute_price(self):
        for rec in self:
            rec.price=rec.property_id.selling_price
    """

    # **** method 2 ****
    price=fields.Float(related='property_id.selling_price',store=True)






# si on veut stocker la valeur on doit utiliser @api.depends car la methode sera executer une seule fois juste au deput (ca va garder la premiere valeure) et sera pas fonctionnelle dans notre cas
# donc on doit faire comme ca

    price=fields.Float(compute='_compute_price',store=True)
    @api.depends('property_id') # quand je change lid de property je vais appeler cette methode pour faire le traitement et le price sera modifier automatiquement
    def _compute_price(self):
        for rec in self:
            rec.price=rec.property_id.selling_price