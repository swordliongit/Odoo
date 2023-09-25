
### Examples:

```xml
<field name="type" attrs="{'invisible': [('name','=', 'AAA')]}" />
```

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
            <button name="set_student_to_rejected" string="Reject Student" type="object" 
            class="oe_highlight"
            attrs="{'invisible':[('status', '=', 'accepted')]}"/>
            ...
```
