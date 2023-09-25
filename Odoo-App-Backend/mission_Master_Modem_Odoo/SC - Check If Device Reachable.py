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

list_modems = env['modem.profile'].search([])
for modem in list_modems:
  update_date = datetime.datetime.strptime(modem.x_update_date, "%d-%m-%Y %H:%M:%S")
  current_datetime = datetime.datetime.now() + datetime.timedelta(hours=3)
  
  # Format current_datetime to match the format of update_date
  current_datetime_formatted = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
  
  # Calculate the time difference in seconds
  time_difference = (datetime.datetime.strptime(current_datetime_formatted, "%Y-%m-%d %H:%M:%S") - update_date).total_seconds()
  log(str([modem.x_mac, update_date, current_datetime_formatted, time_difference]), level='info')
  if abs(time_difference) > 90:
    modem["x_lostConnection"] = True 
  else:
    modem["x_lostConnection"] = False
    
   


