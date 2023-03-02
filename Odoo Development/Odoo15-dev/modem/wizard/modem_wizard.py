# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ModemWizard(models.TransientModel):
    _name = 'modem.wizard'
    _description = "Modem Wizard"
    
    x_ip = fields.Char(string="IP")
    x_subnet = fields.Char(string="Subnet")
    x_dhcp = fields.Boolean(string="DHCP")
    x_enable_wireless = fields.Boolean(string="Enable Wireless")
    x_enable_ssid1 = fields.Boolean(string="Enable SSID1")
    x_enable_ssid2 = fields.Boolean(string="Enable SSID2")
    x_enable_ssid3 = fields.Boolean(string="Enable SSID3")
    x_enable_ssid4 = fields.Boolean(string="Enable SSID4")
    x_manual_time = fields.Char(string="Manual Time")
    x_new_password = fields.Char(string="New Password")
    
    # wizard's save button
    def update_modem_information(self):
        # find active records
        active_ids = self.env.context.get('active_ids', [])
        records = self.env['modem.profile'].browse(active_ids)
        
        x_ip_digits = ""
        # if the user didn't provide any ip, we will skip ip generation
        if self.x_ip != False:
            x_ip_digits = self.x_ip.split('.')
        
        ip_lastdigit_shifter = 0
        for rec in records:
            # generate ips
            if self.x_ip != False:
                rec.write({
                    'x_ip': x_ip_digits[0] + '.' + x_ip_digits[1] + '.' + x_ip_digits[2] + '.' + str(int(x_ip_digits[3])+ip_lastdigit_shifter),
                    'x_subnet': self.x_subnet,
                    'x_dhcp': self.x_dhcp,
                    'x_enable_wireless': self.x_enable_wireless,
                    'x_enable_ssid1': self.x_enable_ssid1,
                    'x_enable_ssid2': self.x_enable_ssid2,
                    'x_enable_ssid3': self.x_enable_ssid3,
                    'x_enable_ssid4': self.x_enable_ssid4, 
                    'x_manual_time': self.x_manual_time,
                    'x_new_password': self.x_new_password,
                })
                ip_lastdigit_shifter+=1
            # don't generate ips
            else:
                rec.write({
                        'x_ip': self.x_ip,
                        'x_subnet': self.x_subnet,
                        'x_dhcp': self.x_dhcp,
                        'x_enable_wireless': self.x_enable_wireless,
                        'x_enable_ssid1': self.x_enable_ssid1,
                        'x_enable_ssid2': self.x_enable_ssid2,
                        'x_enable_ssid3': self.x_enable_ssid3,
                        'x_enable_ssid4': self.x_enable_ssid4, 
                        'x_manual_time': self.x_manual_time,
                        'x_new_password': self.x_new_password,
                    })
        
        all_records = self.env['modem.profile'].search([])
        for rec in all_records:
            rec.write({
                'x_device_update': False
            })
        # close the wizard
        return {'type':'ir.actions.act_window_close'}