# -*- coding: utf-8 -*-
from odoo import models, fields, api


class StudentWizard(models.TransientModel):
    _name = 'student.wizard'
    _description = "Student Wizard"
    
    city = fields.Char(string="City")
    address = fields.Char(string="Address")
    
    # wizard's save button
    def update_student_information(self):
        print("context", self.env.context)
        print("active_id", self.env.context.get("active_id"))
        print("city", self.city)
        print("address", self.address)
        # find the active records
        active_ids = self.env.context.get('active_ids', [])
        records = self.env['student.student'].browse(active_ids)
        for rec in records:
            rec.write({
                'city': self.city,
                'address': self.address
            })
        # close the wizard
        return {'type':'ir.actions.act_window_close'}