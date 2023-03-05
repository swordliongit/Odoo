# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Student(models.Model):
    _name = "student.student"
    _description = "Student Model"

    name = fields.Char(string="Name")
    age = fields.Integer(string="Age")
    email = fields.Char(string="Email")
    join_date = fields.Date(string="Join Date")
    
    school_id = fields.Many2one("school.school", string="School")
    option_ids = fields.Many2many("student.option", string="Options")
    
    address = fields.Char(string="Address")
    city = fields.Char(string="City")
    
    note_1 = fields.Float(string="Note 1")
    note_2 = fields.Float(string="Note 2")
    note_3 = fields.Float(string="Note 3")
    note_4 = fields.Float(string="Note 4")
    
    average = fields.Float(string="Average", compute="get_average_student")
    
    def get_average_student():
        pass
    
class School(models.Model):
    _name = "school.school"
    
    name = fields.Char(string="Name")
    student_ids = fields.One2many("student.student", "school_id", string="Students")
    
    
class StudentOption(models.Model):
    _name = "student.option"
    
    name = fields.Char(string="Name")
    
    