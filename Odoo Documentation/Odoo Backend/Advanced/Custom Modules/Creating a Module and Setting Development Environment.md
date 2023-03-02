### Notes
*Using VS Code*

1. **Write this in cmd and press enter. This will create a custom module template in the target directory**
```
C:\Users\SWORD>"path\to\python.exe" "path\to\odoo-bin" scaffold test_module "path\to\target\directory\"
```
2. **Create a directory and install python venv with python 3.8 in it. Then take the requirements.txt file from the Odoo/server directory and put it inside your newly created workspace folder.**
3. **Install the requirements with**
```python
pip install -r requirements.txt
```
4. **Create *odoo.conf* file inside the directory and put these in it**:
```
[options]
addons_path = C:\Program Files\Odoo 15.0.20221205\server\odoo\addons, C:\Users\SWORD\Desktop\Workspace\Odoo\Odoo Development\Odoo15-dev

;admin_passwd = admin
db_password = openpgpwd
db_user = openpg
;db_port = False
;db_host = False
xmlrpc_port = 8072
logfile = C:\Program Files\Odoo 15.0.20221205\server\odoo.log
dbfilter=
```
addons_path = path/to/odoo/addons, path/to/workspace/directory
5. **Force vscode to create the launch.json file for you by going to Run -> Start Debugging. launch.json should look like this:**
```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python:Odoo",
            "type":"python",
            "request":"launch",
            "stopOnEntry": false,
            "console":"integratedTerminal",
            "program":"C:\\Program Files\\Odoo 15.0.20221205\\server\\odoo-bin",
            "args": [
                "--conf=${workspaceFolder}/odoo.conf",
            ],
            "cwd":"${workspaceFolder}",
            "env": {},
            "envFile":"${workspaceFolder}/.env",
            "redirectOutput": true
        }
    ]
}
```
6. **Run -> Start Without Debugging to start the localserver at the specified port. You should see the server codes. Now you can open the browser with the ==localhost:8072== for example, to open your Odoo app.**
7. **To add your module to the Odoo. Go to Odoo -> Apps -> Update Apps List and you will see your module when you search for it. Install it.