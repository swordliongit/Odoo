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

# create the sale based on the translation
if record['invoice_status'] == "posted":
  sale = env["sale.order"].create({
    'partner_id': record.customer.id,
    'order_line' : [(0, 0, {'product_id': record.product_id.id})],
  })
  sale["state"] = "sale"
  # create the invoice based on the sale
  invoice_vals = sale._prepare_invoice()
  invoice = env['account.move'].create(invoice_vals)
  invoice.write({
    'invoice_line_ids': [(0, 0, {'product_id': record.product_id.id, 'price_unit': sale.order_line.price_unit})]
  })
  invoice.action_post()
  # Reset the invoice payment information
  invoice.write({
      'payment_state': 'not_paid'
  })
  
  
############# V2

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

# create the sale based on the translation
if record['invoice_status'] == "posted":
  currency_name = record.sale_price_currency_id.name
  pricelist = env['product.pricelist'].search([('currency_id.name', '=', currency_name)], limit=1)
  sale = env["sale.order"].create({
    'pricelist_id': pricelist.id,
    'partner_id': record.customer.id,
    'order_line':[
                   [
                      0,
                      "virtual_610",
                      {
                         "product_id": record.product_id.id,
                         "product_template_id": record.product_id.id,
                         "name": record.product_id.name,
                         "product_uom_qty":1,
                         "qty_delivered":1,
                         "qty_delivered_manual":0,
                         "customer_lead":0,
                         "product_packaging_qty":0,
                         "product_packaging_id":False,
                         "price_unit":record.sale_price,
                         "product_id":record.product_id.id,
                      }
                   ]
                  ]
     })
  sale.write({
    'x_translations': [(6, 0, [record.id])]
  })
  sale["state"] = "sale"
  sale._create_invoices()
  for invoice in sale.invoice_ids:
    invoice["invoice_date"] = datetime.datetime.now()
    invoice.write({
    'x_translations': [(6, 0, [record.id])]
    })
    invoice.action_post()