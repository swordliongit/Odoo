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

# find the corresponding link
link = env['links.profile'].search([('card_id', '=', record.x_card_id)], limit=1)
# modify the contact based on the current link's fields
link.write({
  'street': record.street,
  'card_id': record.x_card_id,
  'city': record.city,
  'function': record.function,
  'phone': record.phone,
  'mobile': record.mobile,
  'email': record.email,
  'website': record.website,
  'country_id': record.country_id.id,
  'state': record.state_id.id,
  'card_owner': record.id,
  'users_can_edit': [(6, 0, record.x_users_can_edit.ids)]
})

