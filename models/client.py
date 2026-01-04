from odoo import models


class Client(models.Model):
    # we use this attribut _name if you want create the table in database
    _name ='client'
    _description = 'client'
    # this class "client" herite de la class owner donc va prendre tous les champs declarer dans cette derniere
    _inherit ='owner'

