

1. Go into Postman -> Import -> HTTP Request -> https://limaklara.nitrawork.com/web/session/authenticate as the url. 
2. Go to Headers -> select Key as the ==Content-Type== and Value as ==application/json==
3. Go to Body and paste this, change accordingly and Send the request:
```json
{
        "jsonrpc": "2.0",
        "params": {
            "login": "admin",
            "password": "artinlimak",
            "db": "limaklara"
        }
}
```
4. Import -> https://limaklara.nitrawork.com/web/dataset/call_kw/website/write as the url. Change accordingly.
5. The Body will be shown like this below. ==custom_code_head== key defines the content of the head tag injected. Setting it to empty will clear the content. After that, Send the request:
```json
{"id":9,"jsonrpc":"2.0","method":"call","params":{"args":[[1],{"custom_code_head":""}],"model":"website","method":"write","kwargs":{"context":{"website_id":1,"lang":"en_US"}}}}
```
6. Example response if successful:
```json
{
    "jsonrpc": "2.0",
    "id": 9,
    "result": true
}
```
