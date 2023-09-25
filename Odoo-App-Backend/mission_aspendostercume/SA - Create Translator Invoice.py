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

active_ids = env.context.get('active_ids', [])
selected_records = env['translations.profile'].browse(active_ids)

# Check if all selected records have the same customer
translator_ids = selected_records.mapped('translator.id')
if len(set(translator_ids)) != 1:
  # Display an error message or handle the case when the customers are not the same
  raise UserError("Translators must be the same!!")
else:
  # Create the sale order with combined order lines
  order_lines = []
  for selected_record in selected_records:
    order_line = (0, 0, {
        'product_id': selected_record.product_id.id,
        'product_qty': selected_record.number,
        # Add other necessary fields for the order line
    })
    order_lines.append(order_line)
  purchase = env['purchase.order'].create({
    'partner_id': translator_ids[0],
    'order_line': order_lines,
  })
  # confirm the purchase order
  purchase.button_confirm()
  
  # Create the bill based on the purchase order
  bill_vals = purchase._prepare_invoice()
  bill = env['account.move'].create(bill_vals)
  invoice_lines = []
  for order_line in purchase.order_line:
    invoice_line = (0, 0, {
      'product_id': order_line.product_id.id,
      'quantity': order_line.product_uom_qty,
      'price_unit': order_line.price_unit,
      # Add other necessary fields for the invoice line
    })
    invoice_lines.append(invoice_line)
  
  # Set the invoice date to be one day after creation
  date = datetime.datetime.now() + datetime.timedelta(days=1)
  bill['invoice_date'] = date
  bill.write({
    'invoice_line_ids': invoice_lines
  })
  # confirm the bill
  bill.action_post()



####################### V2


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

active_ids = env.context.get('active_ids', [])
selected_records = env['translations.profile'].browse(active_ids)

# Check if all selected records have the same translator
translator_ids = selected_records.mapped('translator.id')
if len(set(translator_ids)) != 1:
    # Display an error message or handle the case when the translators are not the same
    raise UserError("Translators must be the same!!")
else:
    combined_order_lines = []
    for record in selected_records:
        order_line = (0, 0, {
            'product_id': record.product_id.id,
            'product_qty': record.number,
            'qty_received': record.number,
            'price_unit': record.translator_unit_price,
            # Add other necessary fields for the order line
        })
        combined_order_lines.append(order_line)

    purchase = env['purchase.order'].with_context(default_invoice_status=False).create({
        'partner_id': translator_ids[0],
        'currency_id': selected_records[0].translator_price_currency_id.id,
        'order_line': combined_order_lines,
    })

    # Confirm the purchase order
    purchase.button_confirm()

    purchase.write({
        'x_translations': [(6, 0, selected_records.ids)]
    })

    purchase.action_create_invoice()

    for bill in purchase.invoice_ids:
        bill['invoice_date'] = datetime.datetime.now()

        bill.write({
            'x_translations': [(6, 0, selected_records.ids)]
        })

        bill.action_post()