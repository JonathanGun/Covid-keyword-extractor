# Covid Information Extractor ![Python package](https://github.com/JonathanGun/Covid-keyword-extractor/workflows/Python%20package/badge.svg) [![codecov](https://codecov.io/gh/JonathanGun/Covid-keyword-extractor/branch/master/graph/badge.svg?token=9VS8UYOH0H)](https://codecov.io/gh/JonathanGun/Covid-keyword-extractor)
A simple web app to extract information from plain text made using Flask Python and bootstrap. Program is feeded with keywords and text files.

## Getting Started
## Requirements
1. Python 3.x (tested on 3.6+)
1. Flask
1. WTForms
1. nltk
1. requests (optional - for getting article through link)
1. bs4 (optional)
1. typing (optional - for static analysis)
```
pip install -r requirements.txt
```

## Running
```
python app.py
```
or
```
python3 app.py
```

## Built With
- Flask and WTForms

## Contributing
Feel free to fork and made a pull request, make sure to test it first using pytest

### Testing Program
```
cd src
pip install pytest
pytest
```

## Authors
- Jonathan Yudi Gunawan - Initial work

## Acknowlegdement
This program is made to fulfill IF2211 Strategi Algoritma assessment.

## Live Demo
You can try the program [here](http://covex.herokuapp.com/)
