*Multiple entities to choose from and multiple of them can be selected*


**Create the Many2Many options class**
```python
class StudentOption(models.Model):
    _name = "student.option"
    
    name = fields.Char(string="Name")
```

**Define with what class it will be related by creating the many2many field**
```python
class Student(models.Model):
    _name = "student.student"
    _description = "Student Model"
    
    option_ids = fields.Many2many("student.option", string="Options")
```

**Add the many2many field to where you want to show**
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
              <field name="name"/>
              <field name="school_id"/>
              <field name="age"/>
            </group>
            <group>
              <field name="email"/>
              <field name="join_date"/>
              <field name="option_ids" widget="many2many_tags"/> <!-- Many2many field-->
              ...
              ...
```
**Notes:**
1. *widget* tag is used to make it show as more readable and eye candy, otherwise it looks like the same table-like form of the one2many field.

**Add the security option for the many2many object to the ==ir.model.access.cv==
```
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink

access_for_student_option,Access Student Option,model_student_option,,1,1,1,1
```