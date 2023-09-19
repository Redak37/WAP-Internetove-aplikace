# pekarnaIS

## Dependencies:
* python3 + pip + virtualenv
* nodejs + npm

virtualenv can be installed using pip `python3 -m pip install virtualenv`

## How to run:

```
# Create and activate virtual environment, install python dependencies
python3 -m virtualenv venv
source venv/bin/activate
python3 -m pip install --user -r requirements.txt

# Install nodejs dependencies
npm install --prefix vueapp

# Build vue app
npm run build --prefix vueapp

# Run django server
python3 manage.py runserver
```

For development use `npm run serve`.



## To populate the database with initial data:
`python manage.py filldb` to only insert necessary data
`python manage.py filldb --with_test_data` to also include testing data

or simply use the script `resetdb.sh`