from odoo import models, fields, api


class FirstName(models.AbstractModel):
    _name = 'firstname.mixin'
    _description = 'Mixin for first name'

    last_name = fields.Char()
    first_name = fields.Char()
    full_name = fields.Char(compute='_compute_full_name')

    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for rec in self:
            rec.full_name = self._get_full_name(rec.last_name, rec.first_name)

    def _get_full_name(self, last_name, first_name):
        return "%s (%s)" % (last_name, first_name)
