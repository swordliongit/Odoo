### Notes
	We may want to have states of records and change them based on certain conditions(e.g. a button press)
![[Ti18n_1.png]]
*When Accept Student button pressed:*
![[Ti18n_2.png]]

*To achieve this, create the buttons first:*
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
  <!-- Student Form View -->
  <record id="student_form" model="ir.ui.view">
    <field name="name">Student</field>
    <field name="model">student.student</field>
    <field name="arch" type="xml">
      <form>
        <sheet>
          <header>
            <field name="status" widget="statusbar"/>
            <button name="set_student_to_accepted" string="Accept Student" type="object" class="oe_highlight"/>
            <button name="set_student_to_rejected" string="Reject Student" type="object" class="oe_highlight"/>
          </header>
          <group>
            <group>
            ...
```

Then, create the status field and the function to change the states:
**student_model.py**
```python
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Student(models.Model):
    _name = "student.student"
    _description = "Student Model"
    
    status = fields.Selection([('new', "New"), ('accepted', "Accepted"), ('rejected', "Rejected")], default='new')
    
    def set_student_to_accepted(self):
        template_id = self.env.ref('student.student_accept_email_template')
        print('template_id', template_id)
        self.status = "accepted" 
        if template_id:
            template_id.send_mail(self.id, force_send=True, raise_exception=True, email_values={"email_to": self.email})
            
        
    def set_student_to_rejected(self):
        self.status = "rejected"
```