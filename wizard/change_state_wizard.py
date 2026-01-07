from odoo import models,fields

class ChangeStateWizard(models.TransientModel):
    _name = 'change.state'
    _description = 'Change Property State Wizard'
    property_id=fields.Many2one('property')
    state=fields.Selection([
        ('draft','Draft'),
        ( 'panding','Panding'),
    ],default='draft')
    reason=fields.Char()


    def action_confirm(self):
        if self.property_id.state == 'closed':
            self.property_id.state=self.state
            self.property_id.create_history_record('closed',self.state,self.reason)
            #print('inside action_confirm method')