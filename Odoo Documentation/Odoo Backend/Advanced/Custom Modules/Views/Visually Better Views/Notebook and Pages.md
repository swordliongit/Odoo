**Notebook provides good visual organization to show information specific to each category that are categorized by *page* tags**
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
				<notebook>
					<page string="General Information">
						<h1>Student Information</h1>
						<group>
							<group>
								<field name="address"/>
								<field name="city"/>
							</group>
						</group>
					</page>
					<page string="Notes">
						<group>
							<group>
								<field name="note_1"/>
								<field name="note_2"/>
							</group>
							<group>
								<field name="note_3"/>
								<field name="note_4"/>
							</group>
						</group>
					</page>
				</notebook>
			</sheet>
		</form>
	</field>
</record>
```

### Notes:
1. *notebook* is placed after the first *group* tag so that it appears at the bottom.
2. each notebook page is represented with the *page* tag.
3. *h1* tag is placed to showcase information title.
4. All of them are enclosed in the outside *sheet* tag.

**Result:**
![[notebook.png]]
![[notebook2.png]]
