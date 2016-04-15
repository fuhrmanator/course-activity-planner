# Use in production

This website is highly configured to be used by our organization, but you can alter the source code and use it for yourself. Please keep in mind that respecting the GPL is required or you will be liable to law suits.

Instructions are for Ubuntu 14.04. Should be cloned in /opt as nginx is configured for this path.

It is recommended to install and run the application as a dedicated and unprivileged user.

You are strongly advised to run this application inside a container/VM. Python dependencies will be installed on the system and may cause versioning issues if used with other applications. Contributions are welcomed to use uwsgi and virtualenv.

**Windows is not supported.** See `Windows Help` section in main README.

### Install base system dependencies for Ubuntu 14.04
* `sudo apt-get install npm python3 python3-pip nginx uwsgi uwsgi-plugin-python3 libssl-dev language-pack-fr`
* `sudo npm install grunt-cli -g`

### Install CAP
* `cd /opt`
* `git clone https://github.com/fuhrmanator/course-activity-planner.git`
* `cd course-activity-planner`
* `(cd python && sudo pip3 install -r requirements.txt)`
* `bower install`
* `(cd deploy && npm install)`
* `sudo cp deploy/prod/cap.logti.etsmtl.ca /etc/nginx/sites-enabled/`
* `cp deploy/cap.service /etc/systemd/system/` TODO change for upstart
* Change config/prod_config.py to your needs
* `grunt build`
* `sudo systemctl enable cap` TODO change for upstart
* `sudo systemctl start cap` TODO change for upstart
* `sudo systemctl reload nginx`

## Upgrading CAP
* `sudo systemctl stop cap` TODO change for upstart
* `cd /opt/course-activity-planner/`
* `git pull`
* Run DB migration scripts if needed or delete database
* Change config/prod_config.py to your needs
* `sudo cp deploy/nginx/cap.logti.etsmtl.ca /etc/nginx/sites-enabled/`
* `sudo pip3 install -r requirements.txt`
* `bower install`
* `grunt build`
* `sudo systemctl start cap` TODO change for upstart
* `sudo systemctl reload nginx` TODO change for upstart
