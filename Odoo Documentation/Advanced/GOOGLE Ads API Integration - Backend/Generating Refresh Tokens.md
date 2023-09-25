
## 1. Getting the Client Secret File

1. Go to console.cloud.google.com -> Credentials -> select your app -> download JSON
2. Save the file in your module's folder
3. Create an .env file in the development directory of the Odoo and write these
```json
CLIENT_SECRETS_PATH=robot\client_secret_234984630595-r0qevd34hqsed4lau23i6sm5vuo6naf1.apps.googleusercontent.com.json
OAUTHLIB_RELAX_TOKEN_SCOPE=1
```
Second variable is to avoid getting scope change error when we redirect to the client url at the end.

## 2. Handling Authorize End-Point
```python
# -*- coding: utf-8 -*-
import hashlib
import os
import sys
from google_auth_oauthlib.flow import Flow

module_path = os.path.dirname(os.path.realpath(__file__))
secret_path = os.path.join(module_path, '..', 'secret')
sys.path.append(secret_path)

from secret import Secret

_CLIENT_SECRETS_PATH = os.environ.get("CLIENT_SECRETS_PATH")
_SCOPE = "https://www.googleapis.com/auth/adwords"
_SERVER = "localhost"
_PORT = 8072
_REDIRECT_URI = f"http://{_SERVER}:{_PORT}/oauth2callback"

def authorize():
    flow = Flow.from_client_secrets_file(_CLIENT_SECRETS_PATH, scopes=[_SCOPE])
    flow.redirect_uri = _REDIRECT_URI

    # Create an anti-forgery state token as described here:
    # https://developers.google.com/identity/protocols/OpenIDConnect#createxsrftoken
    passthrough_val = hashlib.sha256(os.urandom(1024)).hexdigest()

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        state=passthrough_val,
        prompt="consent",
        include_granted_scopes="true",
    )
    
    return {"authorization_url": authorization_url, "passthrough_val": passthrough_val}
```
**Notes:**
This function will be called through a controller function and it will set the passthrough key and give access to the authorization url by passing them to the oauth2 end point.

```python
class Oauth2Controller(http.Controller):
    
    @http.route('/authorize', type='http', auth="public", website=True)
    def authorize_endpoint(self):
        auth_info = authorize()
        passthrough_val = auth_info["passthrough_val"]
        http.request.session["passthrough_val"] = passthrough_val
        url = auth_info["authorization_url"]
        return werkzeug.utils.redirect(url)
```

## 3. Handling Oauth2 End-Point

```python
def oauth2callback(passthrough_val, state, code):
    if passthrough_val != state:
        message = "State token does not match the expected state"
        raise ValueError(message)
    
    flow = Flow.from_client_secrets_file(_CLIENT_SECRETS_PATH, scopes=[_SCOPE])
    flow.redirect_uri = _REDIRECT_URI       
    flow.fetch_token(code=code)
    refresh_token = flow.credentials.refresh_token
```
**Notes:**
This function will get the secrets key by checking the passthrough value first, then it will create the refresh token for the app.
```python
@http.route('/oauth2callback', type='http', auth="public", website=True)
    def oauth2callback_endpoint(self, **kw):
        passthrough_val = http.request.session.get("passthrough_val")
        state = kw.get("state")
        code = kw.get("code")
        oauth2callback(passthrough_val, state, code)
        return werkzeug.utils.redirect(_CLIENT_URL)
```

*auth.py:*
```python
# -*- coding: utf-8 -*-
import hashlib
import os
import sys
from google_auth_oauthlib.flow import Flow

module_path = os.path.dirname(os.path.realpath(__file__))
secret_path = os.path.join(module_path, '..', 'secret')
sys.path.append(secret_path)

from secret import Secret

_CLIENT_SECRETS_PATH = os.environ.get("CLIENT_SECRETS_PATH")
_SCOPE = "https://www.googleapis.com/auth/adwords"
_SERVER = "localhost"
_PORT = 8072
_REDIRECT_URI = f"http://{_SERVER}:{_PORT}/oauth2callback"

def authorize():
    flow = Flow.from_client_secrets_file(_CLIENT_SECRETS_PATH, scopes=[_SCOPE])
    flow.redirect_uri = _REDIRECT_URI

    # Create an anti-forgery state token as described here:
    # https://developers.google.com/identity/protocols/OpenIDConnect#createxsrftoken
    passthrough_val = hashlib.sha256(os.urandom(1024)).hexdigest()

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        state=passthrough_val,
        prompt="consent",
        include_granted_scopes="true",
    )
    
    return {"authorization_url": authorization_url, "passthrough_val": passthrough_val}
    
    
def oauth2callback(passthrough_val, state, code):
    if passthrough_val != state:
        message = "State token does not match the expected state"
        raise ValueError(message)
    
    flow = Flow.from_client_secrets_file(_CLIENT_SECRETS_PATH, scopes=[_SCOPE])
    flow.redirect_uri = _REDIRECT_URI       
    flow.fetch_token(code=code)
    refresh_token = flow.credentials.refresh_token(refresh_token)

```

*controllers.py*
```python
# -*- coding: utf-8 -*-
from odoo import http
import werkzeug
import os
import sys

module_path = os.path.dirname(os.path.realpath(__file__))
auth_path = os.path.join(module_path, '..', 'auth')
sys.path.append(auth_path)

from auth import authorize, oauth2callback

_CLIENT_URL = "http://localhost:8072"


class Oauth2Controller(http.Controller):
    @http.route('/authorize', type='http', auth="public", website=True)
    def authorize_endpoint(self, **kw):
        auth_info = authorize()
        passthrough_val = auth_info["passthrough_val"]
        http.request.session["passthrough_val"] = passthrough_val
        url = auth_info["authorization_url"]
        return werkzeug.utils.redirect(url)
    
    @http.route('/oauth2callback', type='http', auth="public", website=True)
    def oauth2callback_endpoint(self, **kw):
        passthrough_val = http.request.session["passthrough_val"]
        state = kw.get("state")
        code = kw.get("code")
        oauth2callback(passthrough_val, state, code)
        return werkzeug.utils.redirect(_CLIENT_URL)
```






## 4. Creating the Authorization Button

To our app to have access to the adwords campaign of the client by authorizing access, we have to redirect to the specific url that we have set, by the aid of a simple button:

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
            <button name="onLinkAdsAccount" onclick="onLinkAdsAccount()" class="btn btn-primary" string="ok"/>
            ...
```

It will call the onLinkAdsAccount javascript function in the googleapp.js that we have created before:
```js
SERVER_URL = ""

function handleLogin(response)
{
    localStorage.setItem("token", response.credential);
    console.log(response);
}

function onLinkAdsAccount()
{
    window.location.href = `${SERVER_URL}/authorize`;
}
```


Lastly, we have to authorize access to the callback url:
![[authredirect.png]]

[[Secret Manager API]]