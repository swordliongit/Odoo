**We may want to generate qr codes for each record and put a button for it that opens the web page with the qr code embedded in it:**
![[idgeneration.png]]
**When you click the button opposite to the field, the web page opens with the qr that has the same link as the ==Contact Id== field:
![[qrpage.png]]

**To achieve this, we have to follow a system:**

### 1. Creating the button and it's function:

```xml
<!--qidgenerator Tree View-->
  <record id="qidgenerator_tree" model="ir.ui.view">
    <field name="name">qidgenerator.tree</field>
    <field name="model">qidgenerator.qidgenerator</field>
    <field name="arch" type="xml">
      <tree>
        <header>
          <button name="%(qidgenerator.qidgenerator_wizard_action)d" string="Id Oluştur" type="action"/>
        </header>
        <field name="cid"/>
        <button name="generateQr" type="object" string="Qr Oluştur" class="oe_link oe_read_only pt-0" /> <!-- button for qr generation-->
      </tree>
    </field>
  </record>
```

```python
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import webbrowser


class QidGenerator(models.Model):
    _name = 'qidgenerator.qidgenerator'
    _description = 'QR ID Generator'

    cid = fields.Char(string="Contact Id")

	# function of the button
    def generateQr(self):
        uuid_from_cid = self.cid.split('/')[-1]
        url = "http://localhost:8072/GET/"+uuid_from_cid
        # url = f"https://www.businesstouch.com.tr/nfc/profile/{uuid_from_cid}"
        webbrowser.open_new(url)
```
**Notes:**
*When the button is pressed, it gets the current record's cid field and takes the last part out of it that is the uuid. Then pastes it after the url address and then opens the url. This way we can send a GET response to Odoo to retrieve the uuid from this url.*

---

### 2. Handling the url and directing to the webpage with a Controller:
```python
# -*- coding: utf-8 -*-
from odoo import http


class QrController(http.Controller):
    
    @http.route('/GET/<cid>', type='http', auth="public", methods=["GET"], cors='*', website=True)
    def my_customers(self, cid):
        return http.request.render("website.contactus_thanks", {'uuid': cid})
```
**Notes:**
*This controller takes the cid field and opens the contactus_thanks page of the website loaded with the data that is a dictionary. We will get the cid field from front end of the website.*

---

### 3. Embedding Qr code in the web page:
```html
<?xml version="1.0"?>
<t name="Thanks (Contact us)" t-name="website.contactus_thanks">
    <t t-call="website.layout">
        <div id="wrap" class="oe_structure oe_empty">
            <section class="s_text_block pt40 pb40 o_colored_level " data-snippet="s_text_block">
                <div class="container s_allow_columns">
                    <div class="row">
                        <div class="col-lg-7 col-xl-6 mr-lg-auto">
                            <div class="pt16 pb16 o_colored_level col-lg-8" style="">
                                <img t-attf-src="/report/barcode/?type=QR&amp;value=https://www.businesstouch.com.tr/nfc/profile/{{uuid}}&amp;width=200&amp;height=200"/>
                            </div>
                            <br/>
                            <h1 class="text-center">Thank You!</h1>
```
**Focus on this part:**
```html
<div class="pt16 pb16 o_colored_level col-lg-8" style="">
    <img t-attf-src="/report/barcode/?type=QR&amp;value=https://www.businesstouch.com.tr/nfc/profile/{{uuid}}&amp;width=200&amp;height=200"/>
 </div>
```
value=https://www.businesstouch.com.tr/nfc/profile/{{uuid}} is the parameter we want to use to embed the link in the Qr code. We access the uuid key of the dictionary that is passed from the controller with =={{uuid}}== at the end of the link.

So whenever this Qr code is scanned, it will redirect to the link that we pass to it.