After [[Prerequisites]],

## 1. Loading Client Library

Go to Google Identity -> Load the client Library and copy the code:
```html
<script src="https://accounts.google.com/gsi/client" async defer></script>
```

For Odoo;
```html
<script src="https://accounts.google.com/gsi/client" async="defer"></script>
```

## 2. Getting Sign-In Button HTML Code

Google Identity -> Code Generator -> Paste your client id and enable one tap option -> Copy the code:
```html
<div id="g_id_onload"
	data-client_id="234984630595-r0qevd34hqsed4lau23i6sm5vuo6naf1.apps.googleusercontent.com"
	data-context="signin"
	data-ux_mode="popup"
	data-callback="handleLogin"
	data-auto_select="true"
	data-itp_support="true">
</div>
<div class="g_id_signin"
	data-type="standard"
	data-shape="rectangular"
	data-theme="outline"
	data-text="signin_with"
	data-size="large"
	data-logo_alignment="left">
</div>
```


After all that, your xml code will look like this, e.g. robot_view.xml:
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
  <!-- robot Form View -->
  <record id="robot_form" model="ir.ui.view">
    <field name="name">robot.form</field>
    <field name="model">robot.profile</field>
    <field name="arch" type="xml">
      <form>
        <sheet>
          <group>
            <script src="https://accounts.google.com/gsi/client" async="defer"></script>
            <div id="g_id_onload"
                data-client_id="234984630595-r0qevd34hqsed4lau23i6sm5vuo6naf1.apps.googleusercontent.com"
                data-context="signin"
                data-ux_mode="popup"
                data-callback="handleLogin"
                data-auto_select="true"
                data-itp_support="true">
            </div>
            <div class="g_id_signin"
                data-type="standard"
                data-shape="rectangular"
                data-theme="outline"
                data-text="signin_with"
                data-size="large"
                data-logo_alignment="left">
            </div>
            <group>
              <field name="url"/>
              ...
```

## 3.Logging the Client

Create a js file under your module/static/src/js/googleapp.js:
```js
function handleLogin(response)
{
    console.log(response);
}
```

Modify the __manifest__.py file to include the js file:
```python
...
# always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/robot_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'robot/static/src/js/googleapp.js',
        ],
    },
...
```

---
## 4. Conclusion

Now you'll see the Google Sign in button, sign in with it and check the inspect -> console to see your information that is written by the js function.

It's time to authorize the app to access client's adwords data:
[[Generating Refresh Tokens]]