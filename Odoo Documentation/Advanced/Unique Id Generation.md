**Let's say we want to achieve the output below in which each record has a unique id with a link:**
![[idgeneration.png]]
**We can create a wizard for this model to do this by selecting 1 record and clicking on the wizard button:**
```python
# -*- coding: utf-8 -*-
from odoo import models, fields, api
import uuid

class QidgeneratorWizard(models.TransientModel):
    _name = 'qidgenerator.wizard'
    _description = "Qidgenerator Wizard"
    
    idcount = fields.Integer(string="Id Adeti")
    
    def generateIds(self):
        """Generate a unique 10-character UID"""
        print("generating")
        for _ in range(self.idcount):
            uuid_str = str(uuid.uuid4())
            self.env['qidgenerator.qidgenerator'].sudo().create({
                'cid': "https://www.businesstouch.com.tr/nfc/profile/" +''.join(uuid_str.split('-')[:4])
            })
            
        # close the wizard
        return {'type':'ir.actions.act_window_close'}
```
