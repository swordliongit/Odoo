# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from odoo import http


class jewelleryProfileReq(http.Controller):
    @http.route('/school_student/school_student/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/all_records_list', type='http', auth='public', website=True)
    def all_Records(self, **kwargs):
        all_records_list = http.request.env['jewellery.profile'].sudo().search([])
        return http.request.render('jewellery.all_records_list', {'my_details': all_records_list})


    @http.route('/dataset/<int:sale_id>', type='http', auth="public", website=True)
    def tracking(self, sale_id):
        # get the information using the SUPER USER
        result = http.request.env['jewellery.profile'].sudo().search([('id','=', sale_id)])
        return http.request.render('jewellery.record_item', {'record_item': result})

    @http.route('/school_student/school_student/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('school_student.listing', {
            'root': '/school_student/school_student',
            'objects': http.request.env['res.users'].search([]),
        })

    @http.route('/school_student/school_student/objects/<model("school_student.school_student"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('school_student.object', {
            'object': obj
        })
