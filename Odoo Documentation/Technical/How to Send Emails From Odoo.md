### Notes
1. Firstly, we have to configure an Outgoing Mail Server for emails to be sent from.
2. Secondly, we have to configure the email itself.


### 1. Configuring Outgoing Mail Server
*We use the mailtrap.io mail server for testing*

1. Go to https://mailtrap.io/
2. Go to Email Testing -> Inboxes
3. SMTP Settings -> Select Ruby on Rails
4. Go to Odoo Technical -> Email -> Outgoing Mail Servers
5. Use the information from the mailtrap.io to fill the username, password, SMTP server and ports: ![[mailtrapio.png]]
	![[mailserver.png]]

### 2. Creating an Email Template
*Place the email's xml file in a folder, e.g. data/student_accept_mail_template.xml*
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <record id="student_accept_email_template" model="mail.template">
            <field name="name">Student Accept Email</field>
            <field name="email_from">{{user.email}}</field>
            <field name="subject">Student Request For Join</field>
            <field name="lang">${object.lang}</field>
            <field name="model_id" ref="model_student_student"/>
            <field name="auto_delete" eval="True"/>
            <field name="body_html">
                <![CDATA[ 
                    Dear Student, <t t-out="object.name"/> <br/>
                    Congrats, you are accepted to join us <t t-out="object.school_id.name"/>
                    <br/>

                    Best regards.
                ]]>
            </field>
        </record>
    </data>
</odoo>
```
*Then we need to trigger this email, e.g. using a button:*
```python
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Student(models.Model):
    _name = "student.student"
    _description = "Student Model"

	...
	...
    
    def set_student_to_accepted(self):
        template_id = self.env.ref('student.student_accept_email_template')
        self.status = "accepted" 
        if template_id:
            template_id.send_mail(self.id, force_send=True, raise_exception=True, email_values={"email_to": self.email})
```
**Notes**
1. *Don't forget that this button is in a view of the model*
2. This configuration is set to work when the accept student button is pressed to accept the student, it sends email to the student in theory.

---
### Gmail Example using only the backend interface
1. Outgoing Mail Server:
	* SMTP Server: smtp.gmail.com
	* SMTP Port: 465
	* Connection Security: SSL/TLS
	* Username: your test email
	* Password: email’s password( create app password after setting 2 step authentication from gmail’s security settings )
	* Test Connection and check if it’s successful
2. Creating Email Template:
	1. Copy an existing mail template for easier time
	2. Edit the content.
	3. From : use {{ user.email_formatted }} -> user is the user of odoo
	4. To (Emails) : {{ object.email_formatted }}
	5. Creating a trigger: Technical -> Automated Actions -> Create
	6. Action to Do: Send Email
	7. Email Template: Select the template that you created
	8. Trigger your action and go to Technical -> Email -> Emails
	9. Check if you have your email ready, send if necessary
