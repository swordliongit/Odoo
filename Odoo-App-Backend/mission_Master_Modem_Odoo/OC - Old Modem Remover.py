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

mac_to_check = record['x_mac']
modems_found = list(env['modem.profile'].search([('x_mac', "=", mac_to_check)]))

if not len(modems_found) == 0 and not len(modems_found) == 1:
  if modems_found[0].create_date < modems_found[1].create_date:
    modems_found[0].unlink()