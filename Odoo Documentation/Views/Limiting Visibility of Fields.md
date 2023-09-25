
### How to make it so that only a specific group can see the field:
```xml
<field name="x_teachers" groups="base.group_system" options="{'no_create': True}"/>
```
**Notes:**
1. base.group_system is the admin
