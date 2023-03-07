### Notes:
1. @api.depends decorator is specifically used for "field.function" in odoo. For a "field.function", you can calculate the value and store it in a field, where it may possible that the calculation depends on some other field(s) of same table or some other table, in that case you can use @api.depends to keep a 'watch' on a field of some table. So, this will trigger the call to the decorated function if any of the fields in the decorator is **'altered by ORM or changed in the form'**.

**Creating a functional Field in the model's class you want**
```python
class Student(models.Model):
    _name = "student.student"
    _description = "Student Model"
	...
    
    average = fields.Float(string="Average", compute="get_average_student")
    
    @api.depends("note_1", "note_2", "note_3", "note_4")
    def get_average_student(self):
        self.average = (self.note_1 + self.note_2 + self.note_3 + self.note_4) / 4
```

**Add it into one of the views to show it**
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
          <notebook>
            <page string="Notes">
              <group>
                ...
                <group>
                  <field name="average"/>
                </group>
                ...
```
