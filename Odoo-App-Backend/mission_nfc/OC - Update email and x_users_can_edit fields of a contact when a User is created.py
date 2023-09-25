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

# find the contact of this user that will be auto-created when this user is created
contact = env['res.partner'].search([('id', '=', record.partner_id.id)], limit=1)
# update the contact; paste the email and id of this user into the corresponding email and ManyToMany fields of this contact
contact.write({
  'email': record.login,
  'x_users_can_edit': [(6, 0, [record.id])]
})