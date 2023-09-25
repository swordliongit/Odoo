**Notes:**
By creating a sequence, we can have a sequence of records based on this sequence.

## 1.Create the Sequence
*sequence_student.xml*
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <record id="sequence_student" model="ir.sequence">
            <field name="name">Student Sequence</field>
            <field name="code">student.sequence</field>
            <field name="prefix">ST</field>
            <field name="padding">5</field>
            <field name="number_next">1</field>
            <field name="number_increment">1</field>
        </record>
    </data>
</odoo>
```

## 2.Create the Inscription Id
```python
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Student(models.Model):
    _name = "student.student"
    _description = "Student Model"

    student_inscription_id=fields.Char(string="Inscription Id")
```

## 3.Display the Inscription Id

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
          <group>
            <group>
              <field name="student_inscription_id" readonly="1"/>
              ...
```

## 4.Modify the Create Function

```python
 @api.model
    def create(self, vals):
        vals['student_inscription_id'] = self.env['ir.sequence'].next_by_code('student.sequence')
        result = super(Student, self).create(vals)
        return result
```
**Notes:**
We assign the next sequence to the newly created record's inscription id field.