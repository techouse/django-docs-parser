# Django docs parser

## Requirements:

- Python 3.4+

## Installation and usage
```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python parser.py
```

The above commands will make a virtual environment in a folder called `env` and install all the requirements listed in `requirements.txt` into that virtual environment.
Once that is done running `python parser.py` will go to the Django documentation for versions __1.11__, __2.1__ and __2.2__, grab their zipped HTML versions and parse them respectively.
It will output a file called `data.json` which you can later use to your avail.

The output JSON file looks like this:
```json
[
  {
    "version": 2.2,
    "id": "django.contrib.postgres.fields.ArrayField",
    "title": "ArrayField",
    "permalink": "https://docs.djangoproject.com/en/2.2/ref/contrib/postgres/fields/#django.contrib.postgres.fields.ArrayField",
    "categories": [
        "class ",
        "contrib",
        "postgres",
        "fields"
    ],
    "content": "A field for storing lists of data. Most field types can be used, you simply pass another field instance as the base_field. You may also specify a size. ArrayField can be nested to store multi-dimensional arrays."
  }
]
```
