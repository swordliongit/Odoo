
**Let's say we want to have the following interactivity:**
![[selection1.png]]
*A status bar is shown at the top right and we have 2 buttons. Accept and Reject. When we want to accept, we press the Accept Student button and the status bar changes its state:*
![[selection2.png]]
*And when we press Reject Student, status bar changes accordingly as well:*
![[selection3.png]]

---

### 1.Creating the status bar and the buttons:
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
            ...
```

### 2.Creating the selection field and the functions of the buttons:
```python
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Student(models.Model):
    _name = "student.student"
    _description = "Student Model"
    
    status = fields.Selection([('new', "New"), ('accepted', "Accepted"), ('rejected', "Rejected")], default='new')
    
    def set_student_to_accepted(self):
        self.status = "accepted"
        
    def set_student_to_rejected(self):
        self.status = "rejected"
```
