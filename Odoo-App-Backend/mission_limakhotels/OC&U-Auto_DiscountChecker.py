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

isFullyDiscounted = True

for answer in record.x_answered_questions:
  if answer.x_discounted != True:
    isFullyDiscounted = False
  
if isFullyDiscounted == True:
  record['x_isFullyDiscounted'] = True
else:
  record['x_isFullyDiscounted'] = False