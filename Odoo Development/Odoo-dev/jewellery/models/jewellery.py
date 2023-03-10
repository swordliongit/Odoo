from odoo import fields, models, api,_
from odoo.exceptions import UserError
import requests
from odoo import http
from odoo.http import request
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)
import json
cookie = "aa"
internal_cookie = "aa"

class jewelleryProfile(models.Model):
    _name = "jewellery.profile"

    name = fields.Char(string="Owner", copy=False, default="Olga")
    jewellery_name = fields.Char("Jewellery Name", copy=False)
    jewellery_degree = fields.Char("Jewellery Degree", copy=False)
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
    jewellery_rank = fields.Integer(string="Rank")
    result = fields.Float(string="Result")
    address = fields.Text(string="Address")
    estalish_date = fields.Date(string="Establish Date")
    open_date = fields.Datetime("Open Date")
    jewellery_type = fields.Selection([('public','Public jewellery'),
                                    ('private', 'Private jewellery')],
                                   string="Type of jewellery",
                                   )
    documents = fields.Binary(string="Documents")
    document_name = fields.Char(string="File Name")
    jewellery_image = fields.Image(string="Upload jewellery Image", max_width=100,
                                max_height=100)
    jewellery_description = fields.Html(string="Description", copy=False)
    auto_rank = fields.Integer(compute="_auto_rank_populate", string="Auto "
                                                                     "Rank",
                               store=True, help="This is auto populate data "
                                                "based on jewellery type change.")

    @api.depends("jewellery_type")
    def _auto_rank_populate(self):
        for rec in self:
            if rec.jewellery_type == "private":
                rec.auto_rank = 50
            elif rec.jewellery_type == "public":
                rec.auto_rank = 100
            else:
                rec.auto_rank = 0

    @api.model
    def name_create(self, name):
        rtn = self.create({"name":name, "email":"abc@gmail.com"})
        return rtn.name_get()[0]

    def name_get(self):
        student_list = []
        for jewellery in self:
            print(self, jewellery)
            name = jewellery.name
            if jewellery.jewellery_type:
                name += " ({})".format(jewellery.jewellery_type)
            student_list.append((jewellery.id, name))
        return student_list
   
    @api.model
    def auth_To_Server(self):
        company = self.env['res.company'].sudo().search([('id','=', 1)])
        for item in company:
            x_url = item.x_url
            x_username = item.x_username
            x_password = item.x_password
            x_database_name = item.x_database_name
        url = 'http://' + x_url + '/web/session/authenticate'
        headers = {
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
            "Content-Type": "application/json"
            }
        myobj = {
            "jsonrpc": "2.0",
            "params": {
                "login": x_username,
                "password": x_password,
                "db": x_database_name
            }
        }
        x = requests.post(url, json = myobj, headers=headers)
        #print the response text (the content of the requested file):
        #return str(x.content)
        #response = x.json()
        #return str(response['jsonrpc'])
        #aşağıdaki işlemle önce json parse edildi sonra 0-52 ye kadar substring yapıldı
        global cookie
        cookie = ((x.headers)['Set-Cookie'])[0:51]
        return str(cookie)
        #-------------------------------------------------------------------

    @api.model
    def auth_To_Internal_Server(self,odoo_url,username,password,db_name):
        url = 'https://' + odoo_url + '/web/session/authenticate'
        headers = {
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
            "Content-Type": "application/json"
            }
        myobj = {
            "jsonrpc": "2.0",
            "params": {
                "login": username,
                "password": password,
                "db": db_name
            }
        }
        x = requests.post(url, json = myobj, headers=headers)
        #print the response text (the content of the requested file):
        #return str(x.content)
        #response = x.json()
        #return str(response['jsonrpc'])
        #aşağıdaki işlemle önce json parse edildi sonra 0-52 ye kadar substring yapıldı
        global internal_cookie
        internal_cookie = ((x.headers)['Set-Cookie'])[0:51]
        return str(internal_cookie)
        #-------------------------------------------------------------------
    
    @api.model
    def start_Scheduled(self,odoo_url,scheduled_url):
        url = 'https://' + odoo_url + scheduled_url
        headers = {
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Cookie": internal_cookie,
            "Upgrade-Insecure-Requests":"1",
            "Accept-Encoding":"gzip, deflate, br"
            }
        x = requests.get(url, headers=headers)
        last_result = (x.content)
        return True

    @api.model
    def get_Inhouse_Customer(self):
        company = self.env['res.company'].sudo().search([('id','=', 1)])
        for item in company:
            x_url = item.x_url
        url = 'https://' + x_url + '/web/dataset/search_read'
        headers = {
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
            "Content-Type": "application/json",
            "Cookie": cookie
            }
        myobj = {
            "jsonrpc":"2.0","method":"call","params":{"model":"hotspot.hotel.guest.in_house","fields":["id","partner_id","display_name_gdpr","birthdate_gdpr","room","check_in_date","check_out_date","email_gdpr","missing_value"],"domain":[],"context":{"lang":"en_US","tz":"Europe/Istanbul","uid":40,"params":{"action":214,"min":1,"limit":80,"view_type":"list","model":"hotspot.hotel.guest.in_house","menu_id":271,"_push_me":0},"bin_size":1},"offset":0,"limit":80,"sort":""},"id":400224464
        }
        x = requests.post(url, json = myobj, headers=headers)
        #print the response text (the content of the requested file):
        #return str(x.content)
        #response = x.json()
        #return str(response['jsonrpc'])
        #aşağıdaki işlemle önce json parse edildi sonra 0-52 ye kadar substring yapıldı
        last_result = json.loads((x.content))['result']['length']
        company = self.env['res.company'].sudo().search([('id','=', 1)])
        for item in company:
            item['x_inhouse_customer_number'] = last_result
        return str(last_result)  

    @api.model
    def get_Project_Departmans(self):
        company = self.env['res.company'].sudo().search([('id','=', 1)])
        for item in company:
            x_url = item.x_url
        url = 'https://' + x_url + '/web/dataset/search_read'
        headers = {
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
            "Content-Type": "application/json",
            "Cookie": cookie
            }
        myobj = {
            "jsonrpc":"2.0","method":"call","params":{"model":"crm.smarttech.department","fields":["partner_id","name","code","description"],"domain":[],"context":{"lang":"tr_TR","tz":"Europe/Istanbul","uid":530,"params":{"action":340,"min":1,"limit":80,"view_type":"list","model":"crm.smarttech.department","menu_id":363,"_push_me":False},"bin_size":True},"offset":0,"limit":80,"sort":""},"id":659880725
        }
        x = requests.post(url, json = myobj, headers=headers)
        #print the response text (the content of the requested file):
        #return str(x.content)
        #response = x.json()
        #return str(response['jsonrpc'])
        #aşağıdaki işlemle önce json parse edildi sonra 0-52 ye kadar substring yapıldı
        last_result = json.loads((x.content))['result']['records']
        company = self.env['res.company'].sudo().search([('id','=', 1)])
        for item in last_result:
            project = self.env['project.project'].sudo().search([('name','=', item['name'])])
            company['x_example_data'] = item['name']
            if len(project) == 0:
                departman_create = request.env['project.project'].sudo().create({
                    'name': item['name']
                })
                task_type_create = request.env['project.task.type'].sudo().create({
                    'name': "Yeni",
                    'project_ids': [departman_create.id]
                })
                task_type_create = request.env['project.task.type'].sudo().create({
                    'name': "Devam Eden",
                    'project_ids': [departman_create.id]
                })
                task_type_create = request.env['project.task.type'].sudo().create({
                    'name': "Bitti",
                    'project_ids': [departman_create.id]
                })
            project = self.env['project.project'].sudo().search([('name','=', "Yeni Talepler")])
            if len(project) == 0:
                departman_create = request.env['project.project'].sudo().create({
                    'name': "Yeni Talepler"
                })
                task_type_create = request.env['project.task.type'].sudo().create({
                    'name': "Yeni",
                    'project_ids': [departman_create.id]
                })
                task_type_create = request.env['project.task.type'].sudo().create({
                    'name': "Devam Eden",
                    'project_ids': [departman_create.id]
                })
                task_type_create = request.env['project.task.type'].sudo().create({
                    'name': "Bitti",
                    'project_ids': [departman_create.id]
                })
        return True

    @api.model
    def get_EmployeesAndCreate(self):
        company = self.env['res.company'].sudo().search([('id','=', 1)])
        for item in company:
            x_url = item.x_url
        url = 'https://' + x_url + '/web/dataset/search_read'
        headers = {
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
            "Content-Type": "application/json",
            "Cookie": cookie
            }
        myobj = {
            "jsonrpc":"2.0","method":"call","params":{"model":"crm.smarttech.staff","fields":["photo","full_name","staff_type","phone1","email","services_list_str","partner_id"],"domain":[],"context":{"lang":"tr_TR","tz":"Europe/Istanbul","uid":530,"params":{"action":339,"min":1,"limit":80,"view_type":"list","model":"crm.smarttech.staff","menu_id":366,"_push_me":False},"bin_size":True},"offset":0,"limit":80,"sort":""},"id":792925411
        }
        x = requests.post(url, json = myobj, headers=headers)
        #print the response text (the content of the requested file):
        #return str(x.content)
        #response = x.json()
        #return str(response['jsonrpc'])
        #aşağıdaki işlemle önce json parse edildi sonra 0-52 ye kadar substring yapıldı
        last_result = json.loads((x.content))['result']['records']
        company = self.env['res.company'].sudo().search([('id','=', 1)])
        for item in last_result:
            employee = self.env['res.users'].sudo().search([('login','=', item['email'])])
            company['x_example_data'] = str(item)
            if len(employee) == 0 and item['email'] != False:
                user = request.env['res.users'].sudo().create({
                    'name': item['full_name'],
                    'login': item['email']
                })
                employee_create = request.env['hr.employee'].sudo().create({
                    'name': item['full_name'],
                    'work_email': item['email'],
                    'mobile_phone': item['phone1'],
                    'job_title': item['services_list_str'],
                    'x_employee_id': item['id'],
                    'user_id': user.id
                })
        return True

    @api.model
    def get_Service_Requests(self):
        company = self.env['res.company'].sudo().search([('id','=', 1)])
        for item in company:
            x_url = item.x_url
        url = 'https://' + x_url + '/web/dataset/search_read'
        headers = {
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
            "Content-Type": "application/json",
            "Cookie": cookie
            }
        myobj = {
            "jsonrpc":"2.0","method":"call","params":{"model":"crm.smarttech.service.demand","fields":["partner_id","service_id","customer_id","customer_room","staff_id","customer_email","customer_explanation","ps_time","statu_color","create_date","evaluation_star","statu"],"domain":[],"context":{"lang":"tr_TR","tz":"Europe/Istanbul","uid":530,"params":{"action":343,"min":1,"limit":80,"view_type":"list","model":"crm.smarttech.service.demand","menu_id":366,"_push_me":False},"bin_size":True},"offset":0,"limit":80,"sort":""},"id":606754870
        }
        x = requests.post(url, json = myobj, headers=headers)
        #print the response text (the content of the requested file):
        #return str(x.content)
        #response = x.json()
        #return str(response['jsonrpc'])
        #aşağıdaki işlemle önce json parse edildi sonra 0-52 ye kadar substring yapıldı
        last_result = json.loads((x.content))['result']['records']
        company = self.env['res.company'].sudo().search([('id','=', 1)])
        for item in last_result:
            if "Çözüm Bekliyor" in item['statu'][1]:
                project = self.env['project.project'].sudo().search([('name','ilike', "Yeni Talep")])
                if item['service_id'] != False:
                    project = self.env['project.project'].sudo().search([('description','ilike', item['service_id'][1])])
                employee = self.env['hr.employee'].sudo().search([('id','=', 1)])
                if item['staff_id'] != False:
                    name_of_employee = item['staff_id'][1]
                    employee = self.env['hr.employee'].sudo().search([('name','=', name_of_employee)])
                    company['x_example_data'] = employee.id
                    if len(employee) == 0:
                        employee = self.env['hr.employee'].sudo().search([('id','=', 1)])

 
                task = self.env['project.task'].sudo().search([('x_project_integration_id','=', item['id'])])
                if len(task) == 0:
                    task_create = request.env['project.task'].sudo().create({
                        'project_id': project.id,
                        'name': item['service_id'][1],
                        'user_ids': [employee.id],
                        'x_customer_name': item['customer_id'][1],
                        'x_customer_email': item['service_id'][1],
                        'x_room_number': item['customer_room'],
                        'description': item['customer_explanation'],
                        'x_request_date': item['create_date'],
                        'x_project_integration_id': item['id']
                    })
        return True

    @api.model
    def write_Service_Requests(self,id):
        task = self.env['project.task'].sudo().search([('x_project_integration_id','=', id)])
        company = self.env['res.company'].sudo().search([('id','=', 1)])
        for item in company:
            x_url = item.x_url
        url = 'https://' + x_url + '/web/dataset/search_read'
        headers = {
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
            "Content-Type": "application/json",
            "Cookie": cookie
            }
        myobj = {
            "jsonrpc":"2.0","method":"call","params":{"model":"crm.smarttech.service.demand.respond.wizard1","method":"create","args":[{"staff_explanation":False,"statu":15}],"kwargs":{"context":{"lang":"tr_TR","tz":"Europe/Istanbul","uid":530,"params":{"action":343},"active_model":"crm.smarttech.service.demand","active_id":task.x_project_integration_id,"active_ids":[task.x_project_integration_id],"search_disable_custom_filters":True}}},"id":296184714
        }
        x = requests.post(url, json = myobj, headers=headers)
        return True

# class resCompanyInherit(models.Model):
#     _inherit = 'res.company'

#     url = fields.Char("Url", copy=False)
#     username = fields.Char("Username", copy=False)
#     password = fields.Char("Password", copy=False)
#     database_name = fields.Char("Database Name", copy=False)

class taskManagerInherit(models.Model):
    _inherit = 'project.task'

    #gender = fields.Selection([('male','Male'),('female', 'Female'),('other', 'Other'),],string="Gender")
    #type_of_person = fields.Selection([('adult','Adult'),('child', 'Child'),('baby', 'Baby'),('driver', 'Driver')],string="Person Type")
    
    # How to OverRide Create Method Of a Model
    # https://www.youtube.com/watch?v=AS08H3G9x1U&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=26
    
    #@api.model
    #def create(self, vals_list):
    #    res = super(ResPartners, self).create(vals_list)
    #    print("yes working")
    #    # do the custom coding here
    #    return res

    @api.model
    def auth_To_Server(self):
        company = self.env['res.company'].sudo().search([('id','=', 1)])
        for item in company:
            x_url = item.x_url
            x_username = item.x_username
            x_password = item.x_password
            x_database_name = item.x_database_name
        url = 'http://' + x_url + '/web/session/authenticate'
        headers = {
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
            "Content-Type": "application/json"
            }
        myobj = {
            "jsonrpc": "2.0",
            "params": {
                "login": x_username,
                "password": x_password,
                "db": x_database_name
            }
        }
        x = requests.post(url, json = myobj, headers=headers)
        #print the response text (the content of the requested file):
        #return str(x.content)
        #response = x.json()
        #return str(response['jsonrpc'])
        #aşağıdaki işlemle önce json parse edildi sonra 0-52 ye kadar substring yapıldı
        global cookie
        cookie = ((x.headers)['Set-Cookie'])[0:51]
        return str(cookie)
        #-------------------------------------------------------------------

    @api.model
    def get_Customer_Birthday(self,date):
        company = self.env['res.company'].sudo().search([('id','=', 1)])
        for item in company:
            x_url = item.x_url
        url = 'https://' + x_url + '/web/dataset/search_read'
        headers = {
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
            "Content-Type": "application/json",
            "Cookie": cookie
            }
        myobj = {
            "jsonrpc":"2.0","method":"call","params":{"model":"hotspot.hotel.guest.in_house","fields":["id","partner_id","display_name_gdpr","birthdate_gdpr","room","check_in_date","check_out_date","email_gdpr","missing_value"],"domain":[["birthday","=",str(date)]],"context":{"lang":"tr_TR","tz":"Europe/Istanbul","uid":530,"params":{"action":214,"min":1,"limit":80,"view_type":"list","model":"hotspot.hotel.guest.in_house","menu_id":271,"_push_me":False},"bin_size":True},"offset":0,"limit":80,"sort":""},"id":888262964
            }
        x = requests.post(url, json = myobj, headers=headers)
        last_result = json.loads((x.content))['result']['records']
        company = self.env['res.company'].sudo().search([('id','=', 1)])
        for item in company:
            item['x_customer_birthday_number'] = json.loads((x.content))['result']['length']
        for item in last_result:
            project = self.env['project.project'].sudo().search([('name','=', "Doğum Günü")])
            task = self.env['project.task'].sudo().search([('x_project_integration_id','=', item['id'])])
            if len(task) == 0:
                task_create = request.env['project.task'].sudo().create({
                    'project_id': project.id,
                    'name': item['room'] + " " + item['display_name_gdpr'] + " " + str(date),
                    'x_customer_name': item['display_name_gdpr'],
                    'x_room_number': item['room'],
                })
        return True

    @api.model
    def get_Customer_Details(self,id,room_number):
        company = self.env['res.company'].sudo().search([('id','=', 1)])
        for item in company:
            x_url = item.x_url
        url = 'https://' + x_url + '/web/dataset/search_read'
        headers = {
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
            "Content-Type": "application/json",
            "Cookie": cookie
            }
        myobj = {
            "jsonrpc":"2.0","method":"call","params":{"model":"hotspot.hotel.guest.in_house","fields":["id","partner_id","display_name_gdpr","birthdate_gdpr","room","check_in_date","check_out_date","email_gdpr","missing_value"],"domain":[["room","=",str(room_number)]],"context":{"lang":"tr_TR","tz":"Europe/Istanbul","uid":997,"params":{"action":227,"id":591376704,"view_type":"form","model":"hotspot.hotel.guest.in_house","menu_id":822,"_push_me":False},"bin_size":True},"offset":0,"limit":80,"sort":""},"id":897114673
        }
        x = requests.post(url, json = myobj, headers=headers)
        #print the response text (the content of the requested file):
        #return str(x.content)
        #response = x.json()
        #return str(response['jsonrpc'])
        #aşağıdaki işlemle önce json parse edildi sonra 0-52 ye kadar substring yapıldı
        if "result" in str(x.content) and "room" in str(x.content):
            last_result = json.loads((x.content))['result']['records']
            company['x_example_data'] = last_result[0]['id']
            self.get_Customer_Agency(last_result[0]['id'],id)
            # task = self.env['project.task'].sudo().search([('id','=', id)])
            # task['activity_summary'] = last_result
            # company = self.env['res.company'].sudo().search([('id','=', 1)])
            # if len(last_result) > 0:
            #     task = self.env['project.task'].sudo().search([('id','=', id)])
            #     for item in last_result:
            #         task['activity_summary'] = last_result[0]['id']
        return True
    
    @api.model
    def get_Customer_Agency(self,customer_id, task_id):
        company = self.env['res.company'].sudo().search([('id','=', 1)])
        for item in company:
            x_url = item.x_url
        url = 'https://' + x_url + '/web/dataset/call_kw/hotspot.hotel.guest.in_house/read'
        headers = {
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
            "Content-Type": "application/json",
            "Cookie": cookie
            }
        myobj = {
            "jsonrpc":"2.0","method":"call","params":{"model":"hotspot.hotel.guest.in_house","method":"read","args":[[customer_id],["unique_key","check_in_date","id","folio","mobil","agency","country_id","language_id","check_out_date","api_key","custom_field_3","custom_field_2","custom_field_1","birthdate_gdpr","custom_field_7","custom_field_6","custom_field_5","custom_field_4","custom_field_9","custom_field_8","name_gdpr","surname_gdpr","discount","is_test_user","nationality","custom_field_10","email_gdpr","hotel_currency_rate","partner_id","room","gender","database_name","passport_gdpr","identity_gdpr","display_name","__last_update"]],"kwargs":{"context":{"lang":"tr_TR","tz":"Europe/Istanbul","uid":997,"params":{"action":227,"id":591376704,"view_type":"form","model":"hotspot.hotel.guest.in_house","menu_id":822,"_push_me":False},"bin_size":True}}},"id":504361175
        }
        x = requests.post(url, json = myobj, headers=headers)
        #print the response text (the content of the requested file):
        #return str(x.content)
        #response = x.json()
        #return str(response['jsonrpc'])
        #aşağıdaki işlemle önce json parse edildi sonra 0-52 ye kadar substring yapıldı
        if "display_name" in str(x.content) and "agency" in str(x.content):
            last_result = json.loads((x.content))['result']
            company['x_example_data'] = last_result[0]['agency']
            if 'x_customer_type' in self.env['project.task']._fields:
                task = self.env['project.task'].sudo().search([('id','=', task_id)])
                task['x_customer_type'] = last_result[0]['agency']
            # task = self.env['project.task'].sudo().search([('id','=', id)])
            # task['activity_summary'] = last_result
            # company = self.env['res.company'].sudo().search([('id','=', 1)])
            # if len(last_result) > 0:
            #     task = self.env['project.task'].sudo().search([('id','=', id)])
            #     for item in last_result:
            #         task['activity_summary'] = last_result[0]['id']
        return True
    
    
    @api.model
    def write_Service_Requests_1(self,id):
        task = self.env['project.task'].sudo().search([('x_project_integration_id','=', id)])
        company = self.env['res.company'].sudo().search([('id','=', 1)])
        for item in company:
            x_url = item.x_url
        url = 'https://' + x_url + '/web/dataset/call_kw/crm.smarttech.service.demand.respond.wizard1/default_get'
        headers = {
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
            "Content-Type": "application/json",
            "Cookie": cookie
            }
        myobj = {
            "jsonrpc":"2.0","method":"call","params":{"model":"crm.smarttech.service.demand.respond.wizard1","method":"default_get","args":[["statu","customer_explanation","demand_id","staff_explanation","service_id"]],"kwargs":{"context":{"lang":"tr_TR","tz":"Europe/Istanbul","uid":530,"params":{"action":343},"active_model":"crm.smarttech.service.demand","active_id":task.x_project_integration_id,"active_ids":[task.x_project_integration_id],"search_disable_custom_filters":True}}},"id":218624413
            }
        x = requests.post(url, json = myobj, headers=headers)
        last_result = json.loads((x.content))
        company['x_example_data'] = last_result
        return True

    @api.model
    def write_Service_Requests_2(self,id):
        task = self.env['project.task'].sudo().search([('x_project_integration_id','=', id)])
        company = self.env['res.company'].sudo().search([('id','=', 1)])
        for item in company:
            x_url = item.x_url
        url = 'https://' + x_url + '/web/dataset/call_kw/crm.smarttech.service.demand.respond.wizard1/onchange'
        headers = {
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
            "Content-Type": "application/json",
            "Cookie": cookie
            }
        myobj = {
            "jsonrpc":"2.0","method":"call","params":{"model":"crm.smarttech.service.demand.respond.wizard1","method":"onchange","args":[[],{"id":False,"demand_id":task.x_project_integration_id,"service_id":False,"customer_explanation":False,"staff_explanation":False,"statu":False},["demand_id","service_id","customer_explanation","staff_explanation","statu"],{"demand_id":"1","service_id":"","customer_explanation":"","staff_explanation":"","statu":""},{"lang":"tr_TR","tz":"Europe/Istanbul","uid":530,"params":{"action":343},"active_model":"crm.smarttech.service.demand","active_id":task.x_project_integration_id,"active_ids":[task.x_project_integration_id],"search_disable_custom_filters":True}],"kwargs":{}},"id":448990043
            }

        x = requests.post(url, json = myobj, headers=headers)
        last_result = json.loads((x.content))
        company['x_example_data'] = last_result
        return True

    
    @api.model
    def write_Service_Requests_3(self,id,statu):
        task = self.env['project.task'].sudo().search([('x_project_integration_id','=', id)])
        company = self.env['res.company'].sudo().search([('id','=', 1)])
        for item in company:
            x_url = item.x_url
        url = 'https://' + x_url + '/web/dataset/call_kw/crm.smarttech.service.demand.respond.wizard1/create'
        headers = {
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
            "Content-Type": "application/json",
            "Cookie": cookie
            }
        myobj = {
            "jsonrpc":"2.0","method":"call","params":{"model":"crm.smarttech.service.demand.respond.wizard1","method":"create","args":[{"staff_explanation":False,"statu":statu}],"kwargs":{"context":{"lang":"tr_TR","tz":"Europe/Istanbul","uid":530,"params":{"action":343},"active_model":"crm.smarttech.service.demand","active_id":task.x_project_integration_id,"active_ids":[task.x_project_integration_id],"search_disable_custom_filters":True}}},"id":256800577
            }

        x = requests.post(url, json = myobj, headers=headers)
        id_result_of_req_3 = json.loads((x.content))['result']
        company['x_example_data'] = id_result_of_req_3

        task = self.env['project.task'].sudo().search([('x_project_integration_id','=', id)])
        company = self.env['res.company'].sudo().search([('id','=', 1)])
        for item in company:
            x_url = item.x_url
        url = 'https://' + x_url + '/web/dataset/call_button'
        headers = {
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
            "Content-Type": "application/json",
            "Cookie": cookie
            }
        myobj = {
            "jsonrpc":"2.0","method":"call","params":{"model":"crm.smarttech.service.demand.respond.wizard1","method":"approve_reservation","domain_id":None,"context_id":1,"args":[[id_result_of_req_3],{"lang":"tr_TR","tz":"Europe/Istanbul","uid":530,"params":{"action":343},"active_model":"crm.smarttech.service.demand","active_id":task.x_project_integration_id,"active_ids":[task.x_project_integration_id],"search_disable_custom_filters":True}]},"id":659794993
            }

        x = requests.post(url, json = myobj, headers=headers)
        last_result = json.loads((x.content))
        #company['x_example_data'] = last_result
        return True


    @api.model
    def get_ReservationsAndCreate(self):
        company = self.env['res.company'].sudo().search([('id','=', 1)])
        for item in company:
            x_url = item.x_url
        url = 'https://' + x_url + '/web/dataset/search_read'
        headers = {
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
            "Content-Type": "application/json",
            "Cookie": cookie
            }
        myobj = {
            "jsonrpc":"2.0","method":"call","params":{"model":"crm.smarttech.alacarte.reservation","fields":["partner_id","customer_id","room","cout","reservation_time","people_count","child_count","restaurant_id","table_id","state"],"domain":[],"context":{"lang":"tr_TR","tz":"Europe/Istanbul","uid":530,"params":{"action":350,"min":1,"limit":80,"view_type":"list","model":"crm.smarttech.alacarte.reservation","_push_me":False},"bin_size":True},"offset":0,"limit":80,"sort":""},"id":318909136
            }
        x = requests.post(url, json = myobj, headers=headers)
        #print the response text (the content of the requested file):
        #return str(x.content)
        #response = x.json()
        #return str(response['jsonrpc'])
        #aşağıdaki işlemle önce json parse edildi sonra 0-52 ye kadar substring yapıldı
        last_result = json.loads((x.content))['result']['records']
        company = self.env['res.company'].sudo().search([('id','=', 1)])
        for item in last_result:
            project = self.env['project.project'].sudo().search([('name','=', "Rezervasyonlar")])
            task = self.env['project.task'].sudo().search([('x_project_integration_id','=', item['id'])])
            if item['state'] == "new":
                if len(task) == 0:
                    task_create = request.env['project.task'].sudo().create({
                        'project_id': project.id,
                        'name': item['restaurant_id'][1],
                        'x_customer_name': item['customer_id'][1],
                        'x_room_number': item['room'],
                        'x_request_date': item['reservation_time'],
                        'x_project_integration_id': item['id']
                    })
        return True

    @api.model
    def send_Push_Notification_With_Playerid(self,auth_key,app_id,player_id,message):
        header = {"Content-Type": "application/json; charset=utf-8",
                  "Authorization": auth_key
                  }
        
        if len(player_id) > 0:
            player_id_list = player_id.split(",")

            payload = {"app_id": app_id,
                    "include_player_ids": player_id_list,
                    "contents": {"en": message},
                    "additionalData": {"urlToOpen": "StaffBadges"}
                    }
            
            req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))

            company = self.env['res.company'].sudo().search([('id','=', 1)])
            company['x_example_data'] = str(req.status_code) + " " + str(req.reason)
            
            print(req.status_code, req.reason)
        
        return True

    @api.model
    def send_Sms(self,usercode,password,msgheader,gsmno,message):
        url = 'https://api.netgsm.com.tr/sms/send/get?usercode='+ usercode + '&password=' + password + '&msgheader=' + msgheader + '&gsmno=' + gsmno + '&message=' + message
        x = requests.get(url)
        return True
        #-------------------------------------------------------------------


        