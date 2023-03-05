1. *Multiple entities to choose from but only 1 can be selected*
2. id is used to select entities
3. Example : Many students go to 1 school


### Creating a Many2one field

*We create the class for it inside the main model's .py file:*
```python
class School(models.Model):
    _name = "school.school"
    
    name = fields.Char(string="Name")
```

*Then we create the related Many2one field in the main class of the module:*
```python
class Student(models.Model):
    _name = "student.student"
    _description = "Student Model"
    
    school_id = fields.Many2one("school.school", string="School")
```

*Lastly, we have to put the field in our views to show it:*
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
              <field name="school_id"/> <!-- Many2one field -->
              <field name="age"/>
            </group>
            ...
            ...
```

---

**Many2one field shows up like this. You can type a name and also create an object of the School class yourself from its menu**

![[many2one.png]]