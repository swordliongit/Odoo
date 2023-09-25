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

# create the purchase based on the translation
if record['translator_invoice_status'] == "posted":
  # create the purchase order
  purchase = env["purchase.order"].with_context(default_invoice_status=False).create({
      'partner_id': record.translator.id,
      'order_line': [(0, 0, {'product_id': record.product_id.id, 'product_qty': record.number, 'qty_received': record.number})]
  })
  # confirm the purchase order
  purchase.button_confirm()
  purchase.write({
        'create_bill': False
  })
  # create the bill
  bill_vals = purchase._prepare_invoice()
  bill = env['account.move'].create(bill_vals)
  # Set the invoice date to be one day after creation
  date = datetime.datetime.now() + datetime.timedelta(days=1)
  bill['invoice_date'] = date
  bill.write({
    'invoice_line_ids': [(0, 0, {'product_id': record.product_id.id, 'quantity': record.number, 'price_unit': purchase.order_line.price_unit})]
  })
  # confirm the bill
  bill.action_post()
  
  ################## V2
  
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

# create the purchase based on the translation
if record['translator_invoice_status'] == "posted":
  purchase = env["purchase.order"].with_context(default_invoice_status=False).create({
      'partner_id': record.translator.id,
      'currency_id': record.translator_price_currency_id.id,
      "order_line":[
                 [
                    0,
                    "virtual_610",
                    {
                       "product_id": record.product_id.id,
                       "product_qty": record.number,
                       "qty_received":record.number,
                       "price_unit": record.translator_unit_price
                    }
                 ]
              ]
      })
  # confirm the purchase order
  purchase.write({
    'x_translations': [(6, 0, [record.id])]
  })
  purchase.button_confirm()
  purchase.action_create_invoice()

  for bill in purchase.invoice_ids:
    bill["invoice_date"] = datetime.datetime.now()
    bill.write({
    'x_translations': [(6, 0, [record.id])]
    })
    bill.action_post()