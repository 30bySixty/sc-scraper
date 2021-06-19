#### pip installs
pip3 install Flask
pip3 install Flask-Script
pip3 install SQLAlchemy
pip3 install Flask-Migrate
pip3 install python-dateutil
pip3 install Flask-Session
pip3 install httplib2
pip3 install requests
pip3 install db.py
pip3 install psycopg2-binary
pip3 install slackclient
pip3 install bs4
pip3 install selenium
pip3 install pycraigslist

#### database setup
$ psql
// create database santacruz;

// if psql: could not connect to server: No such file or directory
// then
// brew services restart postgresql


// if urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED]
// then
// navigate to the Python folder and install certificates