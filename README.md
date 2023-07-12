Star Project
========
- - -

https://xxx.xxx.xxx.xxx:443/					(Whole interface)
https://xxx.xxx.xxx.xxx:443/[profilename]		(Filtered interface)
https://xxx.xxx.xxx.xxx:443/show-screenshots	(Show screenshot)

- - -

This is alpha version so there may be some bugs and unorganized code.

#### Python Library ####
flask
requests
selenium
python-docx
google_auth_oauthlib
google-api-python-client

### User Guide ###
0. Setup requiments packages. (run "install_packages.cmd" file)
1. Congigure environment in "config.py" file.
2. Setup your google API with gmail service and download "credential.json".
3. Copy "credential.json" to "credentials" directory and run "token_generator.py" on local machine
4. Run project (python app.py)

### Special Functions ###
1. Centralized control with gmail.
2. You can choose temp mail method freely. (Temp Gmail, Anonaddy, Minutebox)
3. If you enter no str in name item when create, this create all of your profiles in "users" directory.
4. https://xxx.xxx.xxx.xxx:443/[profilename] use this URL often.

### License ###

MIT

### ChangeLog ###

2023 07 12 - **v3.0.2** 
