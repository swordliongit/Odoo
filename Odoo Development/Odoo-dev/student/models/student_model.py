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
    
    status = fields.Selection([('new', "New"), ('accepted', "Accepted"), ('rejected', "Rejected")], default='new')
    
    average = fields.Float(string="Average", compute="get_average_student")
    
    def set_student_to_accepted(self):
        template_id = self.env.ref('student.student_accept_email_template')
        print('template_id', template_id)
        self.status = "accepted" 
        if template_id:
            template_id.send_mail(self.id, force_send=True, raise_exception=True, email_values={"email_to": self.email})
            
        
    def set_student_to_rejected(self):
        self.status = "rejected"
    
    @api.depends("note_1", "note_2", "note_3", "note_4")
    def get_average_student(self):
        self.average = (self.note_1 + self.note_2 + self.note_3 + self.note_4) / 4

class School(models.Model):
    _name = "school.school"
    
    name = fields.Char(string="Name")
    student_ids = fields.One2many("student.student", "school_id", string="Students")
    
    
class StudentOption(models.Model):
    _name = "student.option"
    
    name = fields.Char(string="Name")
    
    