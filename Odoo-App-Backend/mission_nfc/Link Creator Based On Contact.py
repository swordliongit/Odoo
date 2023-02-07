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

# Find the user for this contact
user = env['res.users'].search([('login', '=', record.email)], limit=1)
# create the link and map each field with the fields in the contact
link = env['links.profile'].create({
        'street': record.street,
        'card_id': record.x_card_id,
        'city': record.city,
        'function': record.function,
        'phone': record.phone,
        'mobile': record.mobile,
        'email': record.email,
        'website': record.website,
        'country_id': record.country_id.id, #ManyToOne
        'state': record.state_id.id, #ManyToOne
        'card_owner': record.id, #ManyToOne
        'users_can_edit': [(6, 0, [user.id])] #ManyToMany
        })


# Alternative:

#ManytoOne fields
country_id = env['res.country'].search([('id', '=', record.id)], limit=1)
card_owner = env['res.partner'].search([('id', '=', record.id)], limit=1)
state_id = env['res.country.state'].search([('id', '=', record.id)], limit=1)
#ManyToMany fields
x_users_can_edit = env['res.users'].search([('login', '=', record.email)], limit=1)
#create the link and map each field with the fields in the contact
link = env['links.profile'].create({
        'street': record.street,
        'card_id': record.x_card_id,
        'city': record.city,
        'function': record.function,
        'phone': record.phone,
        'mobile': record.mobile,
        'email': record.email,
        'website': record.website,
        'country_id': country_id.id,
        'state': state_id.id,
        'card_owner': card_owner.id,
        'users_can_edit': [(6, 0, [x_users_can_edit.id])]
        })