1. *1 entity to choose from but it can have many versions*
2. Example : One school has many students
3. It has its own menu.

### Creating a One2Many Field

*We create the class for it and add the One2Many field:*
```python
class School(models.Model):
    _name = "school.school"
    
    name = fields.Char(string="Name")
    student_ids = fields.One2many("student.student", "school_id", string="Students")
```

*We add the field to the One2Many model's view and create the menu for it:*
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
  <!-- School Form View -->
  <record id="school_form" model="ir.ui.view">
    <field name="name">School</field>
    <field name="model">school.school</field>
    <field name="arch" type="xml">
      <form>
        <sheet>
          <group>
            <group>
              <field name="name"/>
            </group>
            <field name="student_ids"/> <!-- One2many field-->
          </group>
        </sheet>
      </form>
    </field>
  </record>
  <!--School Tree View-->
  <record id="school_tree" model="ir.ui.view">
    <field name="name">School</field>
    <field name="model">school.school</field>
    <field name="arch" type="xml">
      <tree>
        <field name="name"/>
      </tree>
    </field>
  </record>
  <!-- Action to call the views-->
  <record id="school_action" model="ir.actions.act_window">
    <field name="name">School</field>
    <field name="type">ir.actions.act_window</field>
    <field name="res_model">school.school</field>
    <field name="view_mode">tree,form</field>
  </record>
  <!-- School Menu-->
  <menuitem id="school_menu" name="School" sequence="5" action="school_action"/>
</odoo>
```

**Add the security option for the one2many object to the ==ir.model.access.cv==
```
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink

access_for_school,Access School,model_school_school,,1,1,1,1
```

---

**One2many field shows up like this in its own menu:**
![[One2Many_first.png]]

**When you click one ==Add a line== to add a new object, this wizard automatically opens for you:**

![[One2many_second.png]]