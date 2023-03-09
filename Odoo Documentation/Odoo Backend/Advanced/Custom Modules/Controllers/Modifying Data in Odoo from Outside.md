
**Using POST we can send a json object and modify data**
*This controller is triggered when /feedback/ url is opened. It takes the json object and creates a new contact based on the content and returns a json response*
```python
from odoo import http

class FeedbackController(http.Controller):

    @http.route(['/feedback/'], type="json", auth="public", methods=["POST"], csrf=False)
    def feedback(self):
        data = json.loads(http.request.httprequest.data)
        http.request.env['feedback.profile'].sudo().create({
       'name': data['params']['name'],
       'contact_id': data['params']['contact_id'] 
    })
        result = {"status": "OK"}
        return result
```