from odoo import models,fields
from odoo.orm.table_objects import Constraint


class Owner(models.Model):
    _name = "owner"
    _description = "owner"
    name=fields.Char(required=True)
    phone=fields.Char()
    address=fields.Char()
    property_ids=fields.One2many("property","owner_id")

# if you have owners with the same name before you make this constraint you dnt be created in database
    _sql_constraints = [('unique_name', 'unique(name)', 'This name of owner already exists. Please choose another.')]


    #Constraint('unique_name','unique(name)','Name must be unique')

