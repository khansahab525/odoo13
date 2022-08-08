from odoo import fields, models, api


class SallaStore(models.Model):
    _name = 'salla.stores'

    name = fields.Char('Name')
