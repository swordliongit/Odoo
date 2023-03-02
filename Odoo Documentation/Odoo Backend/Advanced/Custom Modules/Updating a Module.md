### Notes
*Changing one of the below requires you to do:*
-  XML changes from Backend interface -> Reload page
-  XML changes from Backend -> Restart server
-  Python -> Restart server, upgrade module
-  JS,CSS -> Reload webpage


**If you modify  your module(security.csv or python), you have to add the --update command to the args list of the launch.json and restart the server to see the changes. Don't forget to remove comment from the __manifest__.py's 'data' key:**
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
                "--update=test_module"
            ],
            "cwd":"${workspaceFolder}",
            "env": {},
            "envFile":"${workspaceFolder}/.env",
            "redirectOutput": true
        }
    ]
}
```