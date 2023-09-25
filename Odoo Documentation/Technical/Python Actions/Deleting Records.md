
### Deleting using the UI:

1. *Automated actions -> Edit Domain -> Enter filters and copy the code, paste into the filter brackets*
```python
env['res.partner'].search([]).unlink()
```
2. *Example filters:*
```python
["&",["country_id.id","=",224],["name","ilike","Ali"]] 
```
3. *Paste into the search() brackets:*
```python
env['res.partner'].search(["&",["country_id.id","=",224],["name","ilike","Ali"]]).unlink()
```

### Deleting using the Unlink method:
```python
env['res.partner'].search([('name', '=', 'Ayşe')]).unlink()
```