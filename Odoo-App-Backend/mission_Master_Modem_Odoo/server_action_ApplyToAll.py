# Available variables:
#  - env: Odoo Environment on which the action is triggered
#  - model: Odoo Model of the record on which the action is triggered; is a void recordset
#  - record: record on which the action is triggered; may be void
#  - records: recordset of all records on which the action is triggered in multi-mode; may be void
#  - time, datetime, dateutil, timezone: useful Python libraries
#  - float_compare: Odoo function to compare floats based on specific precisions
#  - log: log(message, level='info'): logging function to record debug information in ir.logging table
#  - UserError: Warning Exception to use with raise
#  - Command: x2Many commands namespace
# To return an action, assign: action = {...}

counter = 0
x_ip_digits = ""
first = records[0]
for rec in records:
  if counter > 0:
    x_ip_digits = first.x_ip.split('.') 
    rec['x_ip'] = x_ip_digits[0] + '.' + x_ip_digits[1] + '.' + x_ip_digits[2] + '.' + str(int(x_ip_digits[3])+1)
    rec['x_subnet'] = first.x_subnet
    rec['x_dhcp'] = first.x_dhcp
    rec['x_enable_wireless'] = first.x_enable_wireless
    rec['x_enable_ssid1'] = first.x_enable_ssid1
    rec['x_enable_ssid2'] = first.x_enable_ssid2
    rec['x_enable_ssid3'] = first.x_enable_ssid3
    rec['x_enable_ssid4'] = first.x_enable_ssid4
    rec['x_manual_time'] = first.x_manual_time
    rec['x_new_password'] = first.x_new_password
    rec['x_reboot'] = first.x_reboot
  counter+=1