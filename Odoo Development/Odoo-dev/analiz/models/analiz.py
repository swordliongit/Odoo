from odoo import fields, models, api,_
from odoo.exceptions import UserError
import requests
import json
cookie = "aa"

class analizProfile(models.Model):
    _name = "analiz.profile"

    name = fields.Char(string="Name", copy=False)
    room = fields.Char(string="Room", copy=False)
    comment = fields.Char(string="Comment", copy=False)
    x_score_good = fields.Float(string="İyi Yorum Oranı", copy=False)
    x_score_bad = fields.Float(string="Kötü Yorum Oranı", copy=False)
    x_score_neutr = fields.Float(string="Nötr Yorum Oranı", copy=False)
    x_comments_total = fields.Integer(string="Toplam Yorum Sayısı", copy=False)
    x_points_good = fields.Integer(string="İyi Yorum Sayısı", copy=False)
    x_points_bad = fields.Integer(string="Kötü Yorum Sayısı", copy=False)
    x_points_neutr = fields.Integer(string="Nötr Yorum Sayısı", copy=False)
    x_points_nan = fields.Integer(string="Anlamsız Yorum Sayısı", copy=False)
    x_TR_g = fields.Integer(string="İyi Yorum Sayısı", copy=False)
    x_EN_g = fields.Integer(string="İyi Yorum Sayısı", copy=False)
    x_RU_g = fields.Integer(string="İyi Yorum Sayısı", copy=False)
    x_DE_g = fields.Integer(string="İyi Yorum Sayısı", copy=False)
    x_TR_b = fields.Integer(string="Kötü Yorum Sayısı", copy=False)
    x_EN_b = fields.Integer(string="Kötü Yorum Sayısı", copy=False)
    x_RU_b = fields.Integer(string="Yorum Sayısı", copy=False)
    x_DE_b = fields.Integer(string="Kötü Yorum Sayısı", copy=False)
    analiz_name = fields.Char("Analiz Name", copy=False)
    analiz_degree = fields.Char("Analiz Degree", copy=False)
    certificate_date = fields.Date(string="Certificate Date")
    shape = fields.Char("Shape", copy=False)
    carat = fields.Char("Carat", copy=False)
    fluorescence = fields.Char("Fluorescence", copy=False)
    colour_grade = fields.Char("Colour Grade", copy=False)
    clarity_grade = fields.Char("Clarity Grade", copy=False)
    cut = fields.Char("Cut", copy=False)
    colour_grading_scale = fields.Char("Colour Grading Scale", copy=False)
    clarity_grading_scale = fields.Char("Clarity Grading Scale", copy=False)

    email = fields.Char(string="Email", copy=False)
    phone = fields.Char("Phone", copy=False)
    is_virtual_class = fields.Boolean(string="Virtual Class Support?")
    analiz_rank = fields.Integer(string="Rank")
    result = fields.Float(string="Result")
    address = fields.Text(string="Address")
    estalish_date = fields.Date(string="Establish Date")
    open_date = fields.Datetime("Open Date")
    analiz_type = fields.Selection([('public','Public analiz'),
                                    ('private', 'Private analiz')],
                                   string="Type of analiz",
                                   )
    documents = fields.Binary(string="Documents")
    document_name = fields.Char(string="File Name")
    analiz_image = fields.Image(string="Upload analiz Image", max_width=100,
                                max_height=100)
    analiz_description = fields.Html(string="Description", copy=False)
    auto_rank = fields.Integer(compute="_auto_rank_populate", string="Auto "
                                                                     "Rank",
                               store=True, help="This is auto populate data "
                                                "based on analiz type change.")
