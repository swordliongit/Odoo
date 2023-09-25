**Simple Models/student.py**
```python
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Student(models.Model):
    _name = 'student.student'
    _description = 'student.student'

    name = fields.Char(string="Name")
    age = fields.Integer(string="Age")
    email = fields.Char(string="Email")
    join_date = fields.Date(string="Join Date")
```

---

### 1. Create the Views

**Inside the views/yourviewname.xml**
*Form view*
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Student Form View -->
    <record id="student_form" model="ir.ui.view">
        <field name="name">Student</field>
        <field name="model">student.student</field>
        <field name="arch" type="xml">
            <form>
                <field name="name"/>
                <field name="age"/>
                <field name="email"/>
                <field name="join_date"/>
            </form>
        </field>
    </record>
</odoo>
```
**Notes:**
1. *record* tag creates a new record of object in the model's database.
2. *ir.ui.view* is the model template you want this object to inherit from.
3. *name* is the *model's name*
4. *model* is the *description* of your model's class
5. *arch* indicates the *xml data*
6. After you provide these informations, you have to provide the *form* tag to create your form with the fields you want to use from your model's class.
**Tree view**
```xml
    <record id="student_tree" model="ir.ui.view">
        <field name="name">Student</field>
        <field name="model">student.student</field>
        <field name="arch" type="xml">
            <tree>
                <field name="name"/>
                <field name="age"/>
                <field name="email"/>
                <field name="join_date"/>
            </tree>
        </field>
    </record>
```
**Notes:**
1. Only difference here is the *tree* tag that requests a tree view

---

### 2. Create the Action To Call the Views

**To show the views in the backend, an action needs to be created to call the views**
```xml
<!-- Action to call the views-->
<record id="student_action" model="ir.actions.act_window">
	<field name="name">Student</field>
	<field name="type">ir.actions.act_window</field>
	<field name="res_model">student.student</field>
	<field name="view_mode">tree,form</field>
</record>
```
**Notes:**
1. *record* tag creates a new record of object in the model's database.
2. *ir.actions.act_window is the model template you want this object to inherit from.
3. *name* is the *model's name*
4. *type* is the action's type
5. *res_model* is the *resource model* for this action to use that is the description of your model's class
6. *view_mode* determines which views to include. It's ordered and the order is determined by *tree,form*

---

### 3. Create the Menu Item for the Action
```xml
<menuitem id="student_menu" name="Student" sequence="4" action="student_action"/>
```
**Notes:**
1. Creating the menu item will place a menu in the *Home Menu* in the backend that can be clicked. Once clicked, it will call the *action* specified in the tag.

---

### 4. Complete Example:

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Student Form View -->
    <record id="student_form" model="ir.ui.view">
        <field name="name">Student</field>
        <field name="model">student.student</field>
        <field name="arch" type="xml">
            <form>
                <field name="name"/>
                <field name="age"/>
                <field name="email"/>
                <field name="join_date"/>
            </form>
        </field>
    </record>

    <!--Student Tree View-->
    <record id="student_tree" model="ir.ui.view">
        <field name="name">Student</field>
        <field name="model">student.student</field>
        <field name="arch" type="xml">
            <tree>
                <field name="name"/>
                <field name="age"/>
                <field name="email"/>
                <field name="join_date"/>
            </tree>
        </field>
    </record>

  
    <!-- Action to call the views-->
    <record id="student_action" model="ir.actions.act_window">
        <field name="name">Student</field>
        <field name="type">ir.actions.act_window</field>
        <field name="res_model">student.student</field>
        <field name="view_mode">tree,form</field>
    </record>

    <menuitem id="student_menu" name="Student" sequence="4" action="student_action"/>

</odoo>
```