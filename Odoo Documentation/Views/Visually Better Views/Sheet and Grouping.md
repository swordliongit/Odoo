**To create visually better views, we can *group* fields together**:
*Form View*
```xml
<!-- Student Form View -->
<record id="student_form" model="ir.ui.view">
	<field name="name">Student</field>
	<field name="model">student.student</field>
	<field name="arch" type="xml">
		<form>
			<group>
				<group>
					<field name="name"/>
					<field name="age"/>
				</group>
				<group>
					<field name="email"/>
					<field name="join_date"/>
				</group>
			</group>
		</form>
	</field>
</record>
```
**Think each group tag's id like this:**
1 | 2
3 | 4
5 | 6

**Result:**![[Screenshot 2023-03-02 115043.png]]

**To further beautify the view, we can use *sheet* to further separate the form from the base of the box:**
*Form View*
```xml
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
                            <field name="age"/>
                        </group>
                        <group>
                            <field name="email"/>
                            <field name="join_date"/>
                        </group>
                    </group>
                </sheet>
            </form>
        </field>
    </record>
```
**Result:**
![[Screenshot 2023-03-02 115715.png]]