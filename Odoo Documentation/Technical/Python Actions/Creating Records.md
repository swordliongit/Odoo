## Examples

#### Creating a Contact whenever a Sale is created:
```python
contact_title = env['res.partner.title'].search([('name', '=', 'Mister')], limit=1)
company_name = env['res.partner'].search([('name', '=', 'Ali Özer')], limit=1)
company_name_filtered_by_mobile = env['res.partner'].search([('phone', '=', '0555')], limit=1)

contact = env['res.partner'].create({
        'name': 'newcustomer',
        'parent_id': company_name_filtered_by_mobile.id,
        'company_type': 'person',
        'function': 'Employee',
        'phone': '',
        'mobile': '+901232321',
        'email': 'abc@mail.com',
        'website': '',
        'title': contact_title.id,
        'category_id': False
    })

```

#### Creating a Sale with 15 days payment term and Ayşe as the customer name:
```python
sale_customer = env['res.partner'].search([('name', '=', 'Ayşe')], limit=1)
payment_term = env['account.payment.term'].search([('name', '=', "15 Days" )], limit=1)

sale = env['sale.order'].create({
        'partner_id': sale_customer.id,
        'validity_date': False,
        'date_order': datetime.datetime.now(),
        'payment_term_id': payment_term.id
    })

```

#### Creating a contact with a ManyToMany field in it:
```python
contacts = env['res.partner'].create({
        'name': 'newcustomer',
        'parent_id': False,
        'company_type': 'person',
        'function': 'Employee',
        'phone': '',
        'mobile': '+901232321',
        'email': 'abc@mail.com',
        'website': '',
        'title': False,
        'category_id': [(6, 0, [1, 2])]
        })

```