#### Overwriting a Sale and changing its name and adding an expiration date whenever a contact is created:
```python
sale_to_modify = env['sale.order'].search([('partner_id', '=', 'Ayşe')], limit=1)
name_to_paste = env['res.partner'].search([('name', '=', 'Ali Özer')], limit=1)

sale_to_modify.write({
        'partner_id': name_to_paste.id,
        'validity_date': datetime.datetime.now(),
        'date_order': datetime.datetime.now(),
    })
```

#### Modifying a ManyToMany field of a record based on another record, inserting multiple tags:
```python
link.write({
  'users_can_edit': [(6, 0, record.x_users_can_edit.ids)]
})

```

#### Modifying a ManyToOne field of a record based on another record:
```python
link.write({
  'country_id': record.country_id.id,
})
```

#### Modifying a Contact when a User is created:
```python
# find the contact of this user that will be auto-created when this user is created
contact = env['res.partner'].search([('id', '=', record.partner_id.id)], limit=1)
# update the contact; paste the email and id of this user into the corresponding email and ManyToMany fields of this contact
contact.write({
  'email': record.login,
  'x_users_can_edit': [(6, 0, [record.id])]
})
```

#### Creating a sale and updating the OneToMany field:
```python
customer_name = env['res.partner'].search([('name', '=', 'Ali Özer')], limit=1)
product = env['product.template'].search([('name', '=', 'Kamera 1')], limit=1)
product2 = env['product.template'].search([('name', '=', 'Kamera 2')], limit=1)

sale = env['sale.order'].create({
        'partner_id': customer_name.id,
        'date_order': datetime.datetime.now()
        })
sale.write({
   'order_line' : [(0, 0, {'product_id': product.id, 'name': product.name, 'product_uom_qty': 5, 'price_unit': 100})]
})
sale.write({
   'order_line' : [(0, 0, {'product_id': product2.id, 'name': product2.name, 'product_uom_qty': 2, 'price_unit': 70})]
})
```

