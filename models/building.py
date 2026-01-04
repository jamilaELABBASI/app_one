from odoo import models,fields

class Building(models.Model):
    _name='building'
    _description='building'
    _inherit=['mail.thread','mail.activity.mixin']
    _rec_name = 'code' # le nom qui saffiche a cote du boutton new au moment denregistrement dun record
    name=fields.Char()
    active=fields.Boolean(default=True) # pour activer loption archive
    no=fields.Integer()
    code=fields.Char()
    description=fields.Text()

