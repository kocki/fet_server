# FET Server

## Development setup

#### In development dir  initially:
```
# Create virtualenv
python3 -m venv venv
source venv/bin/activate

# Fetch repo
git clone git@github.com:kocki/fet_server.git

cd fet_server

# install dependencies
pip install -r requirements/develop.txt

# init:
# Prepare API_KEY for fixer.io
echo "FIXER_API_KEY = 'API_KEY'" > project/settings_local.py
./manage.py migrate
./manage.py runserver
```

or
```
# Fetch repo
git clone git@github.com:kocki/fet_server.git
./fet_server/bin/develop.sh
# replace API_KEY in project/settings_local.py
```


#### Testing:
```
py.test --cov --cov-report term-missing:skip-covered
```


## To Do
* CI/CD setup
