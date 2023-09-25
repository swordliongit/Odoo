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
customer_ids = selected_records.mapped('customer.id')
if len(set(customer_ids)) != 1:
  # Display an error message or handle the case when the customers are not the same
  raise UserError("Customers must be the same!!")
else:
  # Create the sale order with combined order lines
  order_lines = []
  for selected_record in selected_records:
    order_line = (0, 0, {
        'product_id': selected_record.product_id.id,
        'product_uom_qty': selected_record.number,
        # Add other necessary fields for the order line
    })
    order_lines.append(order_line)
    
  sale = env['sale.order'].create({
    'partner_id': customer_ids[0],
    'order_line': order_lines,
  })
  sale['state'] = "sale"
  # Create the bill based on the sale order
  invoice_vals = sale._prepare_invoice()
  invoice = env['account.move'].create(invoice_vals)
  
  invoice_lines = []
  for order_line in sale.order_line:
    invoice_line = (0, 0, {
      'product_id': order_line.product_id.id,
      'quantity': order_line.product_uom_qty,
      'price_unit': order_line.price_unit,
      # Add other necessary fields for the invoice line
    })
    invoice_lines.append(invoice_line)
  
  invoice.write({
    'invoice_line_ids': invoice_lines
  })
  #invoice['invoice_line_ids'] = invoice_lines
  invoice.action_post()

  # Reset the invoice payment information
  invoice['payment_state'] = 'not_paid'


#################### V2

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
customer_ids = selected_records.mapped('customer.id')
if len(set(customer_ids)) != 1:
    # Display an error message or handle the case when the customers are not the same
    raise UserError("Customers must be the same!!")
else:
    combined_order_lines = []
    for record in selected_records:
        currency_name = record.sale_price_currency_id.name
        pricelist = env['product.pricelist'].search([('currency_id.name', '=', currency_name)], limit=1)
        order_line = (0, 0, {
            'product_id': record.product_id.id,
            'product_template_id': record.product_id.id,
            'name': record.product_id.name,
            'product_uom_qty': 1,
            'qty_delivered': 1,
            'qty_delivered_manual': 0,
            'customer_lead': 0,
            'product_packaging_qty': 0,
            'product_packaging_id': False,
            'price_unit': record.sale_price,
        })
        combined_order_lines.append(order_line)

        sale = env["sale.order"].create({
            'pricelist_id': pricelist.id,
            'partner_id': record.customer.id,
            'order_line': combined_order_lines,
        })

        sale.write({
            'x_translations': [(6, 0, selected_records.ids)]
        })

        sale['state'] = "sale"
        sale._create_invoices()

        for invoice in sale.invoice_ids:
            invoice['invoice_date'] = datetime.datetime.now()
            invoice.write({
                'x_translations': [(6, 0, selected_records.ids)]
            })
            invoice.action_post()

            # Reset the invoice payment information
            invoice['payment_state'] = 'not_paid'


#################### V3

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

for item in selected_records:
    if item.invoice_status == "posted":
        raise UserError(("Tek Faturada Birleştirmeye Çalıştığınız Çevirinin Biri veya Birkaçının Müşteri Faturası Önceden Zaten Kesilmiş! Faturası Kesilmemiş Olan Çevirileri Seçiniz!"))

# Check if all selected records have the same customer
customer_ids = selected_records.mapped('customer.id')
if len(set(customer_ids)) != 1:
    # Display an error message or handle the case when the customers are not the same
    raise UserError("Customers must be the same!!")
else:
    combined_order_lines = []
    currency_name = selected_records[0].sale_price_currency_id.name
    pricelist = env['product.pricelist'].search([('currency_id.name', '=', currency_name)], limit=1)

    for record in selected_records:
        order_line = (0, 0, {
            'product_id': record.product_id.id,
            'product_template_id': record.product_id.id,
            'name': record.product_id.name,
            'product_uom_qty': 1,
            'qty_delivered': 1,
            'qty_delivered_manual': 0,
            'customer_lead': 0,
            'product_packaging_qty': 0,
            'product_packaging_id': False,
            'price_unit': record.sale_price,
        })
        combined_order_lines.append(order_line)

    sale = env["sale.order"].create({
        'pricelist_id': pricelist.id,
        'partner_id': selected_records[0].customer.id,
        'order_line': combined_order_lines,
    })

    # Update the translations field for the sale order
    sale.write({
        'x_translations': [(6, 0, selected_records.ids)]
    })

    # Confirm the sale order
    sale.action_confirm()

    # Create an invoice for the sale order
    invoice = sale._create_invoices()

    # Set the invoice date and update the translations field for the invoice
    invoice['invoice_date'] = datetime.datetime.now()
    invoice.write({
        'x_translations': [(6, 0, selected_records.ids)]
    })

    # Post the invoice and reset the payment state
    invoice.action_post()
    invoice['payment_state'] = 'not_paid'