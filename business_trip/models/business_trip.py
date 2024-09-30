# -*- coding: utf-8 -*-

from odoo import models, fields, _


class BusinessTrip(models.Model):
    _name = 'business.trip'
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
        'firstname.mixin'
    ]
    _description = 'Business Trip'

    name = fields.Char(tracking=True, required=True)
    partner_id = fields.Many2one('res.partner', 'Responsible',
                                 tracking=True)
    guest_ids = fields.Many2many('res.partner', 'Participants')
    state = fields.Selection(
        [('draft', 'New'), ('confirmed', 'Confirmed')],
        default='draft',
        tracking=True
    )
    
    def action_confirm(self):
        self.ensure_one()
        self.message_subscribe((self.guest_ids|self.partner_id).ids)
        self.state = 'confirmed'

    def action_cancel(self):
        self.ensure_one()
        self.message_unsubscribe(self.guest_ids.ids)
        self.state = 'draft'

    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'state' in init_values and self.state == 'confirmed':
            return self.env.ref('business_trip.mt_state_change')
        return super(BusinessTrip, self)._track_subtype(init_values)
