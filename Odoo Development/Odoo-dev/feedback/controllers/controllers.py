# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from odoo import http
# from odoo.http import request, Response, route, JsonRequest
from datetime import datetime,date
import logging
import requests
import json
_logger = logging.getLogger(__name__)
from odoo.tools import date_utils


class FeedbackController(http.Controller):
    
    @http.route(['/feedback/<name>'], type="http", auth="public", methods=["GET"], csrf=False)
    def feedback(self):
        return "Hello World"
    
    @http.route('/GET/<email>', type='http', auth="public", methods=["GET"], cors='*', website=False)
    def write_Playerid(self, email):
        contact = http.request.env['res.partner'].sudo().search([["email", "=", email]],limit=1)

        response = {'job': contact.function, 'phone': contact.phone}
        return json.dumps(response)

    @http.route(['/feedback/'], type="json", auth="public", methods=["POST"], csrf=False)
    def feedback(self):
        data = json.loads(http.request.httprequest.data)
        http.request.env['feedback.profile'].sudo().create({
       'name': data['params']['name'],
       'contact_id': data['params']['contact_id'] 
    })
        result = {"status": "OK"}
        return result