### Notes:
1. We can send data to Odoo using GET or POST methods and also retrieve data with the same methods but there are a few distinctions we have to follow.
2. ==GET== is used for viewing something, without changing it.
3. ==POST== is used for changing something.



### GET -> [[Viewing Data in Odoo From Outside]]

==GET is used to request data from a specified resource.==

Note that the query string (name/value pairs) is sent in the URL of a GET request:

/test/demo_form.php?name1=value1&name2=value2
**Some notes on GET requests:**

GET requests can be cached
GET requests remain in the browser history
GET requests can be bookmarked
GET requests should never be used when dealing with sensitive data
GET requests have length restrictions
GET requests are only used to request data (not modify)

---

### POST -> [[Modifying Data in Odoo from Outside]]

==POST is used to send data to a server to create/update a resource.==

The data sent to the server with POST is stored in the request body of the HTTP request:

POST /test/demo_form.php HTTP/1.1
Host: w3schools.com

name1=value1&name2=value2
**Some notes on POST requests:**

POST requests are never cached
POST requests do not remain in the browser history
POST requests cannot be bookmarked
POST requests have no restrictions on data length
