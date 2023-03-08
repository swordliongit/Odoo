# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Feedback(models.Model):
    _name = 'feedback.profile'
    _description = 'Feedback Module'

    name = fields.Char(string="Name")
    contact_id = fields.Many2one('res.partner', string="Contact ID")
    
    
