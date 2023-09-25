
**Using POST we can send a json object and modify data**
*This controller is triggered when /feedback/ url is opened. It takes the json object and creates a new contact based on the content and returns a json response*
```python
from odoo import http

class FeedbackController(http.Controller):

    @http.route(['/feedback/'], type="json", auth="public", methods=["POST"], csrf=False)
    def feedback(self):
        data = json.loads(http.request.httprequest.data)
        http.request.env['feedback.profile'].sudo().create({
       'name': data['params']['name'],
       'contact_id': data['params']['contact_id'] 
    })
        result = {"status": "OK"}
        return result
```

**We can do 2 different POSTs. One is creating a post request directly  to Odoo(slower). The other one is posting and handling it with a controller(faster)

## Direct POST Example:

## **1. Logging in to Odoo:**
```python
def odoo_login():
    url = 'https://modem.nitrawork.com/web/session/authenticate'
    headers = {
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
        "Content-Type": "application/json"
    }
    myobj = {
        "jsonrpc": "2.0",
        "params": {
            "login": "admin",
            "password": "Artin.modems",
            "db": "modems"
        }
    }
    x = requests.post(url, json=myobj, headers=headers)
    global cookie
    cookie = ((x.headers)['Set-Cookie'])[0:51]

    print(cookie)
```
**Notes:**
1. *Specify login, password and db keys to login to your database. This function also prints the cookie.*

## **2. Creating a POST request:**

**Template for the POST:**
```python
def send_datato_odoo_one_by_one():
    url = 'http://localhost:8069/web/dataset/call_kw/modem.profile/create'
    headers = {
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
        "Content-Type": "application/json",
        "Cookie": cookie
    }
    myobj = "" # this will be filled with our data
    
    x = requests.post(url, json=myobj, headers=headers)
```
**Notes:**
1. We'll fill ==myobj== variable with our data that we want to send to Odoo.

**Creating the json data for sending**

Assume that we want to create records based on the fields we want from an outside source. We have to replicate the create function.
1. Just before pressing Create,
	1. Right Click -> Inspect -> Network -> Create -> you'll see create event below -> Right Click -> Copy -> Copy as cURL( bash )
	2. Open ==Postman== -> Import -> Raw Text -> paste the cURL -> Continue -> Import
	3. Copy the created url and go to the POST template above and give it to the myobj variable:
```python
def odooPost():
    url = 'http://localhost:8069/web/dataset/call_kw/modem.profile/create'
    headers = {
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
        "Content-Type": "application/json",
        "Cookie": cookie
    }
    myobj = {"id":43,"jsonrpc":"2.0","method":"call","params":{

        "args":[

            {"partner_gid":0,"additional_info":False,"image_1920":False,"__last_update":False,"is_company":False,"active":True,"company_type":"person","name":"proto5","parent_id":False,"company_name":False,"type":"contact","street":False,"street2":False,"city":False,"state_id":False,"zip":False,"country_id":False,"vat":False,"x_uptime":False,"x_wireless_status":False,"x_channel":False,"x_mac":False,"x_ip":False,"x_device_info":False,"x_subnet":False,"x_dhcp":False,"x_enable_wireless":False,"x_enable_ssid1":False,"x_enable_ssid2":False,"x_enable_ssid3":False,"x_enable_ssid4":False,"x_manual_time":False,"x_new_password":False,"x_wan_status":False,"x_lan_info":False,"phone":False,"mobile":False,"user_ids":[],"email":False,"message_follower_ids":[],"activity_ids":[],"message_ids":[]

             }

            ],
        "model":"res.partner","method":"create","kwargs":{"context":{"lang":"tr_TR","tz":"Europe/Istanbul","uid":2,"allowed_company_ids":[1],"params":{"cids":1,"menu_id":96,"action":122,"model":"res.partner","view_type":"kanban"},"default_is_company":True}}}}
    x = requests.post(url, json=myobj, headers=headers)
```
**Notes:**
1. "args" key has a list containing all of the fields of the model. We can modify them according to what we need for the record to have.
2. Don't forget to change true and false to ==True and False==.


## **3. Execute the functions:**
1. Now we want to first login() and then odooPost(). We'll see the record created with the fields we modified.

---

## Controller POST Example:

## **1. Creating a POST Request:**

```python
def odooPost(modem_data: dict):
    # need to check this for multiple databases position
    url = 'https://modem.nitrawork.com/create/modems_from_data'
    headers = {
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
        "Content-Type": "application/json",
        "Cookie": cookie
    }

    requests.post(url, json=modem_data, headers=headers)
```
**Notes:**
1. Controller will handle the url and fetch the json object that we'll send with it.
2. json data is passed to this function like this:
	```python
	modem_read_result_list = {"modems":[]}	        
		while not read_queue.empty():
			modem_read_result_list["modems"].append(read_queue.get())
			
		odooPost(modem_read_result_list)

	```
3. "modems" key replicates the "args" key of the json object. It will contain the fields in a list.

## **2. Creating the Controller:**
```python
class CreateModemsController(http.Controller):
    @http.route(['/create/modems_from_data'], type="json", auth="public", methods=["POST"], cors='*', csrf=False)
    def modem_data_send(self):
        data = json.loads(request.httprequest.data)
        for modem in data["modems"]:
            http.request.env['modem.profile'].sudo().create({
                'x_uptime': modem['x_uptime'],
                'x_wireless_status': modem['x_wireless_status'],
                'x_channel': modem['x_channel'],
                'x_mac': modem['x_mac'],
                'x_device_info': modem['x_device_info'],
                'x_ip': modem['x_ip'],
                'x_subnet': modem['x_subnet'],
                'x_dhcp': modem['x_dhcp'],
                'x_enable_wireless': modem['x_enable_wireless'],
                'x_enable_ssid1': modem['x_enable_ssid1'],
                'x_enable_ssid2': modem['x_enable_ssid2'],
                'x_enable_ssid3': modem['x_enable_ssid3'],
                'x_enable_ssid4': modem['x_enable_ssid4'], 
                'x_manual_time': modem['x_manual_time'],
                'x_new_password': modem['x_new_password'],
                'x_hotel_name': modem['x_hotel_name'],
                'x_update_date': modem['x_update_date']
            })
```
**Notes:**
1. We catch the url and take the json object out of it using the json.loads function and then we iterate over it to create as many records as there are in "modems" key's list.