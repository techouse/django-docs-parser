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
Once that is done running `python parser.py` will go to the Django documentation for versions __1.11__ and __2.1__, grab their zipped HTML versions and parse them respectively.
It will output a file called `data.json` which you can later use to your avail.