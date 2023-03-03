# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Student(models.Model):
    _name = 'student.student'
    _description = 'Student Model'

    name = fields.Char(string="Name")
    age = fields.Integer(string="Age")
    email = fields.Char(string="Email")
    join_date = fields.Date(string="Join Date")
    
    address = fields.Char(string="Address")
    city = fields.Char(string="City")
    
    note_1 = fields.Float(string="Note 1")
    note_2 = fields.Float(string="Note 2")
    note_3 = fields.Float(string="Note 3")
    note_4 = fields.Float(string="Note 4")
    
    
    
    
    