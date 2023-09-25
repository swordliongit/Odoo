Documentation: https://cloud.google.com/secret-manager/docs/samples/secretmanager-create-secret

## 1. Getting the token from the Javascript function

In the googleapp.js file, we get the token that was stored by the handleLogin function and we add a query parameter after 'authorize' so we can get that token out of the url when we want:
```python
function onLinkAdsAccount()
{
    token = localStorage.getItem("token");
    window.location.href = `${SERVER_URL}authorize?token=${token}`;
}
```

## 2. Catching the token and giving it to the Session.

*controllers.py*

Getting the token and setting it to the current Session. We also give the token to the oauth2callback function as an argument:
```python
class Oauth2Controller(http.Controller):
    @http.route('/authorize', type='http', auth="public", website=True)
    def authorize_endpoint(self, **kw):
        token = kw.get("token") #
        http.request.session["token"] = token #
        auth_info = authorize()
        passthrough_val = auth_info["passthrough_val"]
        http.request.session["passthrough_val"] = passthrough_val
        url = auth_info["authorization_url"]
        return werkzeug.utils.redirect(url)
    
    @http.route('/oauth2callback', type='http', auth="public", website=True)
    def oauth2callback_endpoint(self, **kw):
        token = http.request.session["token"] #
        passthrough_val = http.request.session["passthrough_val"]
        state = kw.get("state")
        code = kw.get("code")
        oauth2callback(passthrough_val, state, code, token) #
        return werkzeug.utils.redirect(_CLIENT_URL)
```

*auth.py*
```python
def oauth2callback(passthrough_val, state, code, token):
	...
```

## 3. Creating and Storing Secrets

1. Setting env variables in .env file:
```json
CLIENT_SECRETS_PATH=robot\client_secret_234984630595-r0qevd34hqsed4lau23i6sm5vuo6naf1.apps.googleusercontent.com.json
OAUTHLIB_RELAX_TOKEN_SCOPE=1
CLIENT_ID=234984630595-r0qevd34hqsed4lau23i6sm5vuo6naf1.apps.googleusercontent.com
PROJECT_NUMBER=234984630595
PROJECT_ID=odoo-integration-test-385807
```

2. Creating a Secret class and validate method:

Create a folder "secret" and inside we have "__init__.py" and "secret.py":
*secret.py:*
```python
import os
import google_crc32c

from google.oauth2 import id_token
from google.auth.transport import requests
from google.cloud import secretmanager

_CLIENT_ID = os.environ.get("CLIENT_ID")
_PROJECT_ID = os.environ.get("PROJECT_ID")
_PROJECT_NUMBER = os.environ.get("PROJECT_NUMBER")

class Secret:
    def __init__(self, token):
         # Get ID from token
         self.id = self.validate_token_get_id(token)
         self.client = secretmanager.SecretManagerServiceClient()
         
    def validate_token_get_id(self, token):
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), _CLIENT_ID)
            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            # If auth request is from a G Suite domain:
            # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')
            # ID token is valid. Get the user's Google Account ID from the decoded token.
            return idinfo['sub']
        except ValueError:
            # Invalid token
            pass
```

3. Creating the secret version:
```python
 def create_secret_version(self, refresh_token):
        # Check if secret exists
        # If not create a secret
        if self.does_secret_exist() is False:
            # If not create a secret
            # Build the resource name of the parent project.
            parent = f"projects/{_PROJECT_ID}"
            
            response = self.client.create_secret(
                request={
                    "parent": parent,
                    "secret_id": self.id,
                    "secret": {"replication": {"automatic": {}}},
                }
            )
            print("Created secret: {}".format(response.name))
        # Create secret version under secret
        # Build the resource name of the parent secret.
        parent = self.client.secret_path(_PROJECT_ID, self.id)
        # Convert the string payload into a bytes. This step can be omitted if you
        # pass in bytes instead of a str for the payload argument.
        payload = refresh_token.encode("UTF-8")
        # Calculate payload checksum. Passing a checksum in add-version request
        # is optional.
        crc32c = google_crc32c.Checksum()
        crc32c.update(payload)
        # Add the secret version.
        self.client.add_secret_version(
            request={
                "parent": parent,
                "payload": {"data": payload, "data_crc32c": int(crc32c.hexdigest(), 16)},
            }
        )
```

3. Checking if Secret exists:
```python
def does_secret_exist(self):
        # Build the resource name of the parent project.
        parent = f"projects/{_PROJECT_ID}"
        # List all secrets.
        for secret in self.client.list_secrets(request={"parent": parent}):
            secret_name = f"projects/{_PROJECT_NUMBER}/secrets/{self.id}"
            if secret.name == secret_name:
                return True
            
        return False
```

4. Getting the Secret version:
```python
def get_secret_version(self):
        # Build the resource name of the secret version.
        name = f"projects/{_PROJECT_ID}/secrets/{self.id}/versions/latest"
        # Access the secret version.
        response = self.client.access_secret_version(request={"name": name})
        # Verify payload checksum.
        crc32c = google_crc32c.Checksum()
        crc32c.update(response.payload.data)
        if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
            print("Data corruption detected.")
            return response
        # Print the secret payload.
        #
        # WARNING: Do not print the secret in a production environment - this
        # snippet is showing how to access the secret material.
        return response.payload.data.decode("UTF-8")
```

Whole secret/secret.py:
```python
import os
import google_crc32c

from google.oauth2 import id_token
from google.auth.transport import requests
from google.cloud import secretmanager

_CLIENT_ID = os.environ.get("CLIENT_ID")
_PROJECT_ID = os.environ.get("PROJECT_ID")
_PROJECT_NUMBER = os.environ.get("PROJECT_NUMBER")

class Secret:
    def __init__(self, token):
         # Get ID from token
         self.id = self.validate_token_get_id(token)
         self.client = secretmanager.SecretManagerServiceClient()
         
    def validate_token_get_id(self, token):
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), _CLIENT_ID)
            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            # If auth request is from a G Suite domain:
            # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')
            # ID token is valid. Get the user's Google Account ID from the decoded token.
            return idinfo['sub']
        except ValueError:
            # Invalid token
            pass
        
    def create_secret_version(self, refresh_token):
        # Check if secret exists
        # If not create a secret
        if self.does_secret_exist() is False:
            # If not create a secret
            # Build the resource name of the parent project.
            parent = f"projects/{_PROJECT_ID}"
            
            response = self.client.create_secret(
                request={
                    "parent": parent,
                    "secret_id": self.id,
                    "secret": {"replication": {"automatic": {}}},
                }
            )
            print("Created secret: {}".format(response.name))
        # Create secret version under secret
        # Build the resource name of the parent secret.
        parent = self.client.secret_path(_PROJECT_ID, self.id)
        # Convert the string payload into a bytes. This step can be omitted if you
        # pass in bytes instead of a str for the payload argument.
        payload = refresh_token.encode("UTF-8")
        # Calculate payload checksum. Passing a checksum in add-version request
        # is optional.
        crc32c = google_crc32c.Checksum()
        crc32c.update(payload)
        # Add the secret version.
        self.client.add_secret_version(
            request={
                "parent": parent,
                "payload": {"data": payload, "data_crc32c": int(crc32c.hexdigest(), 16)},
            }
        )
        
    def does_secret_exist(self):
        # Build the resource name of the parent project.
        parent = f"projects/{_PROJECT_ID}"
        # List all secrets.
        for secret in self.client.list_secrets(request={"parent": parent}):
            secret_name = f"projects/{_PROJECT_NUMBER}/secrets/{self.id}"
            if secret.name == secret_name:
                return True
            
        return False
    
    def get_secret_version(self):
        # Build the resource name of the secret version.
        name = f"projects/{_PROJECT_ID}/secrets/{self.id}/versions/latest"
        # Access the secret version.
        response = self.client.access_secret_version(request={"name": name})
        # Verify payload checksum.
        crc32c = google_crc32c.Checksum()
        crc32c.update(response.payload.data)
        if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
            print("Data corruption detected.")
            return response
        # Print the secret payload.
        #
        # WARNING: Do not print the secret in a production environment - this
        # snippet is showing how to access the secret material.
        return response.payload.data.decode("UTF-8")
```

## 3. Check the Created Secrets:
1. Install the "Google Cloud Code" extension from VS Code, login in to the Secret Manager and select your cloud project. You will see the generated secret.


Next step: [[Google Ads API Setup]]