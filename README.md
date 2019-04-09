# FET Server

## Development setup

####In developement dir:
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

#### Testing:
```
py.test --cov --cov-report term-missing:skip-covered
```
