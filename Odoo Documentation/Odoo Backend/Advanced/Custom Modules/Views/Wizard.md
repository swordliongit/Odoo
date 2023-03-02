**Wizards allow us to modify record data easier**

### 1. First, we have to create the model for the wizard in module/wizard/ folder
```python
# -*- coding: utf-8 -*-
from odoo import models, fields, api


class StudentWizard(models.TransientModel):
    _name = 'student.wizard'
    _description = "Student Wizard"
    
    city = fields.Char(string="City")
    address = fields.Char(string="Address")
    
    # wizard's save button
    def update_student_information(self):
	    return
```
**Notes:**
1. For example, we want to modify the *city* and *address* fields of the record.
2. *update_student_information* method will do the actual modification and will be filled later.

---

### 2. Create the view and action for the wizard in module/wizard/modelname_wizard.xml
*Wizard Action*
```xml
<!-- Wizard's Action-->
<record id="student_wizard_action" model="ir.actions.act_window">
	<field name="name">Update Student Information</field>
	<field name="type">ir.actions.act_window</field>
	<field name="res_model">student.wizard</field>
	<field name="view_mode">form</field>
	<field name="target">new</field>
</record>
```
**Notes:**
1. *res_model* is the model name of the wizard object
2. *view_mode* is the view type of the wizard
3. *target* defines the action when this wizard is triggered

*Wizard View*
```xml
<!-- Wizard's view-->
<record id="student_wizard_view" model="ir.ui.view">
	<field name="name">student.wizard.form</field>
	<field name="model">student.wizard</field>
	<field name="arch" type="xml">
		<form>
			<group>
				<group>
					<field name="city"/>
					<field name="address"/>
				</group>
			</group>
			<footer>
				<button string="Save" name="update_student_information" type="object" class="btn-primary"/>
				<button string="Reject" class="btn-default" special="cancel"/>
			</footer>
		</form>
	</field>
</record>
```
**Notes:**
1. *model* is the model name of the wizard object
2. We encompass what we want to show on the wizard panel inside the *form* tag.
3. We create a *footer* tag to place the *Save* and *Reject* buttons at the bottom.
4. *name* attribute of the button defines the method to call( method of the StudentWizard class)

*student_wizard.xml*
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <!-- Wizard's Action-->
        <record id="student_wizard_action" model="ir.actions.act_window">
            <field name="name">Update Student Information</field>
            <field name="type">ir.actions.act_window</field>
            <field name="res_model">student.wizard</field>
            <field name="view_mode">form</field>
            <field name="target">new</field>
        </record>
        <!-- Wizard's view-->
        <record id="student_wizard_view" model="ir.ui.view">
            <field name="name">student.wizard.form</field>
            <field name="model">student.wizard</field>
            <field name="arch" type="xml">
                <form>
                    <group>
                        <group>
                            <field name="city"/>
                            <field name="address"/>
                        </group>
                    </group>
                    <footer>
                        <button string="Save" name="update_student_information" type="object" class="btn-primary"/>
                        <button string="Reject" class="btn-default" special="cancel"/>
                    </footer>
                </form>
            </field>
        </record>
    </data>
</odoo>
```

---

### 3.Create the button that will call the wizard
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
                        <!-- <field name="status" widget="statusbar"/> -->
                        <button name="%(test_module.student_wizard_action)d" string="Update Student Information" type="action"/>
                    </header>
		            ...
		            ...
		            ...
		        </sheet>
		    </form>
		</field>
	</record>
	...
	...
</odoo>
```
**Notes:**
1. We place the button at the top layer of the form by using the *header* tag
2. We place the button in the *header* tag.
3. Button's name calls the *student_wizard_action* that was set in the *student_wizard.xml* by using that special syntax to look in the module's directory.

---

### 4.Define the wizard's function
```python
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
        # find the active record
        record = self.env['student.student'].browse(self.env.context.get("active_id"))
        record.write({
            'city': self.city,
            'address': self.address
        })
        # close the wizard
        return {'type':'ir.actions.act_window_close'}
```

---

### 5.Put an init.py file inside the wizard folder and import the wizard
```python
# -*- coding: utf-8 -*-
from . import student_wizard
```

---

### 6.Modify init.py and manifest.py of the module to include the wizard folder and wizard's xml files
*init.py*
```python
# -*- coding: utf-8 -*-

from . import controllers
from . import models
from . import wizard
```
*manifest.py*
```python
...
# always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/student_wizard.xml',
        'views/student_view.xml',
    ],
...
```