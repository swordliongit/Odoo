# Copyright 2022 ELITE Advanced technologies.
# Copyright 2022 ELITE - Salim ROUMILI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, api, models, _


class ResUsers(models.Model):
    _inherit = 'res.users'

    ks_multiplier = fields.Float(string="Commission", default=0)