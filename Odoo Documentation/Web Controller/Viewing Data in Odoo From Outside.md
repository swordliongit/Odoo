
**Using GET request to view data and return a json string:**
*It takes the email and searches the contact of this email and returns the job and name fields in json format. To trigger this controller, webappurl/GET/email* url must be opened.
```python
from odoo import http
import json

class FeedbackController(http.Controller):
    
    @http.route('/GET/<email>', type='http', auth="public", methods=["GET"], cors='*', website=False)
    def write_Playerid(self, email):
        contact = http.request.env['res.partner'].sudo().search([["email", "=", email]],limit=1)

        response = {'job': contact.function, 'phone': contact.phone}
        return json.dumps(response)
```
**Notes:**
1. This controller returns a json response when a request is made to .../GET/email. 
2. ==email== is a query string variable and is passed to the function that is wrapped by the @http.route decorator.
