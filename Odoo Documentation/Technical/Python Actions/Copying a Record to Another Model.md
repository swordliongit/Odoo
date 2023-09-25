e.g Contact -> Link

```python
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
        # paste the user id list from the MtM field into the MtM field of this link
        # single [(6, 0, [record.x_users_can_edit.id])] caused an internal server error
        'users_can_edit': [(6, 0, record.x_users_can_edit.ids)]
        })     
```