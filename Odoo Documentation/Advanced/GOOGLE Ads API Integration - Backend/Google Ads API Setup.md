
## 1. Add the Environment Variables
```json
DEVELOPER_TOKEN=5HvuZqdJ72BQLH9suPJpJQ
CLIENT_SECRET=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
```


## 2. Creating the Google Ads Runner

*ga_runner.py:*
```python
import os

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from secret.secret import Secret

_VERSION = "v13"


def create_client(token):
    try:
        secret = Secret(token)
        refresh_token = secret.get_secret_version()
        credentials = {
            "developer_token": os.environ.get("DEVELOPER_TOKEN"),
            "client_id": os.environ.get("CLIENT_ID"),
            "client_secret": os.environ.get("CLIENT_SECRET"),
            "refresh_token": refresh_token,
            "use_proto_plus": "true"
        }
        return GoogleAdsClient.load_from_dict(credentials, version=_VERSION)
    except:
        raise ValueError("INVALID REFRESH TOKEN")


def handleGoogleAdsException(ex: GoogleAdsException):
    print(
        f'Request with ID "{ex.request_id}" failed with status '
        f'"{ex.error.code().name}" and includes the following errors:'
    )
    for error in ex.failure.errors:
        print(f'\tError with message "{error.message}".')
        if error.location:
            for field_path_element in error.location.field_path_elements:
                print(f"\t\tOn field: {field_path_element.field_name}")
```