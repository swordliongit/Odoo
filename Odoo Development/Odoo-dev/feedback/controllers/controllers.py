# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from odoo import http
from odoo.http import request, Response, route, JsonRequest
from datetime import datetime,date
import logging
import requests
import json
_logger = logging.getLogger(__name__)
from odoo.tools import date_utils


class FeedbackController(http.Controller):

    @http.route(['/feedback/'], type="json", auth="public", methods=["POST"], csrf=False)
    def feedback(self):
        data = json.loads(request.httprequest.data)
        invoice = request.env['feedback.profile'].sudo().create({
       'name': data['params']['name'],
       'contact_id': data['params']['contact_id'] 
    })
        result = {"status": "OK"}
        return result