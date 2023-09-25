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

answers = []
# iterate over each answer and put name and point into a dictionary. answers list will have dictionaries as its elements.
for answer in record.x_answered_questions:
  answers.append({answer.name: answer.x_point})

# iterate over each dictionary in the list
for answer in answers:
  # iterate over each key-value pair in the dictionary
  for name, point in answer.items():
    env['project.task'].create({
      'project_id': 49,
      'name': name,
      'x_contact': record.id,
      'x_customer_email': record.email,
      'x_room_number': record.x_room_number,
      'x_points': point
    })  

#for answer in answers:
#  log(str(answer), level="info")