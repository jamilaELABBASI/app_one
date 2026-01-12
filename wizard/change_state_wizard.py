from odoo import models, fields, api

class ChangeStateWizard(models.TransientModel):
    _name = 'change.state'
    _description = 'Change Property State Wizard'

    property_id = fields.Many2one(
        'property',
        readonly=True
    )

    reason = fields.Char(required=True)

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('pending', 'Pending'),
            ('sold', 'Sold'),
            ('closed', 'Closed'),
        ],
        required=True
    )

    def action_confirm(self):
        for rec in self:
            old_state=rec.property_id.state
            new_state=rec.state
            if old_state != new_state:
                # Mettre à jour le champ state du record
                rec.property_id.state=new_state
                # Créer l'historique
                rec.property_id.create_history_record(old_state,new_state,rec.reason)