
### Split the email via @ and log the name and domain seperately:
```python
if "@" in record.email:
  parsed = record.email.split("@")
  str_to_pass = "Name: " + parsed[0] + " Domain: " + parsed[1]
else:
  raise UserError("Lütfen emailde @ sembolünü kullanın!!") 

log(str_to_pass, level = "info")
```

### Split the email via @ and log the name and domain seperately:
```python
if "kcl_" in record.name and "pcl_" in record.name:
  if record.name.index("kcl_") == 0:
    prefix = record.name.index("kcl_") + 4
    postfix = record.name.index("pcl_")
    name_to_fetch = record.name[prefix:postfix]
    if len(name_to_fetch) > 0:
      log(name_to_fetch, level = "info")
    else:
      raise UserError("Boş isim girdiniz!!")
  else:
    raise UserError("Lütfen kcl_ ve pcl_ sıralamasını karıştırmayın!!")
else:
  raise UserError("Lütfen kcl_ ve pcl_ yi unutmayın!!")
```