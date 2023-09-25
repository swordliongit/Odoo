## Examples

#### Contacts – Country changer according to phone number
```python
for rec in records:
  if "+90" in rec.mobile:
    rec["country_id"] = 224
```

#### Contacts - Number converter:
```python
for rec in records:
  if "Olga" in rec.name:
    rec["mobile"] = "+790"
```

#### Contacts - Bad words warning:
```python
for rec in records:
  if "şerefsiz" in rec.comment or "salak" in rec.comment:
   raise osv.except_osv(_('warning'), _('Lütfen uygun kelimeler kullanın!!'))
```

#### Contacts – Logging sales amount when a contact is created:
```python
List_Record = env['sale.order'].search([])
log(str(len(List_Record)), level='info')
Sales app - Combining Quotation date with a custom field named “x_sales_detail”:
for rec in records:
  rec["x_sales_detail"] =  "Camera Was sold in " + rec.date_order.strftime('%m/%d/%Y')
```

#### Sales app - Showing in logs if the sale date has passed or not:
```python
for rec in records:
  if rec.date_order < datetime.datetime.now():
    log("Satışın tarihi geçti", level='info')
  else:
    log("Satışın tarihi gelmedi", level='info')
```

#### Sales app – Show in logs if the person that has the sale is from Turkey or Not:
```python
for rec in records:
  if rec.partner_id.country_id.id == 224:
    log("Bu kişi Türktür", level='info')
  else:
    log("Bu kişi Türk değildir", level='info')
```