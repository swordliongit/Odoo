### Notes
1. *We may need to retrieve a recordset as a json object. To do this, we can do a POST request to Odoo to return us the recordset*

## 1.Catching the search_read Data from Odoo
*We have to get the json format of the search_read function from google that captures all of the recordset.*
1. Navigate to some other page
2. Right Click -> Inspect -> Network -> Clear
3. Navigate to the page you want to capture
4. Check actions from the developer tools menu and look for ==search_read==
5. Right click on search_read -> Copy -> Copy as cURL(bash)
6. Go into ==Postman== > Import -> Raw Text -> paste your data
7. Now take this json object and give it the myobj variable below:

## 2.Creating a POST Request
```python
def fetch_datafrom_odoo():
    url = 'https://modem.nitrawork.com/web/dataset/search_read'
    headers = {
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
        "Content-Type": "application/json",
        "Cookie": cookie
    }
    myobj = {"id": 20, "jsonrpc": "2.0", "method": "call", "params": {"model": "modem.profile", "domain": [["x_device_update", "=", True]], "fields": ["x_hotel_name", "x_update_date", "x_uptime", "x_wireless_status", "x_channel", "x_mac", "x_device_info", "x_ip", "x_subnet", "x_dhcp", "x_enable_wireless", "x_enable_ssid1", "x_enable_ssid2", "x_enable_ssid3", "x_enable_ssid4", "x_manual_time", "x_new_password", "x_reboot", "name", "modem_status", "city", "live_status"], "limit": 80, "sort": "live_status DESC", "context": {"lang": "en_US", "tz": "Europe/Istanbul", "uid": 2, "allowed_company_ids": [1], "params": {"cids": 1, "menu_id": 129, "action": 182, "model": "modem.profile", "view_type": "list"}, "bin_size": True}}}
    # to access our modems : last_result['result']['records'][0] -> gives the first dict

    x = requests.post(url, json=myobj, headers=headers)
    last_result = json.loads((x.content))
    print(str(last_result))
    
    return last_result['result']['records']

```
**Notes:**
1. When we run this function, Odoo will return the request with a json object in this format:
```python
{'jsonrpc': '2.0', 'id': 39, 'result': {'length': 2, 'records': [{'id': 5, 'x_uptime': False, 'x_wireless_status': False, 'x_channel': False, 'x_mac': False, 'x_device_info': False, 'x_ip': False, 'x_subnet': False, 'x_dhcp': False, 'x_enable_wireless': True, 'x_enable_ssid1': False, 'x_enable_ssid2': False, 'x_enable_ssid3': False, 'x_enable_ssid4': False, 'x_manual_time': False, 'x_new_password': False, 'name': 'protomet', 'modem_status': False, 'city': False, 'live_status': 'offline'}, {'id': 6, 'x_uptime': False, 'x_wireless_status': False, 'x_channel': False, 'x_mac': False, 'x_device_info': False, 'x_ip': False, 'x_subnet': False, 'x_dhcp': True, 'x_enable_wireless': False, 'x_enable_ssid1': False, 'x_enable_ssid2': False, 'x_enable_ssid3': False, 'x_enable_ssid4': False, 'x_manual_time': False, 'x_new_password': False, 'name': 'protomet2', 'modem_status': False, 'city': False, 'live_status': 'offline'}]}}
```
2. That means we have successfully read the whole recordset and we can use it now.
3. =='records'== key will contain each record as a dictionary and to get one of them we can index into it:
```python
last_result['result']['records'][0]
```