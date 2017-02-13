# Giscademy
Django application for doing codecademy style tutorials for GIS.
[![Build Status](https://travis-ci.org/RubenSchmidt/giscademy.svg?branch=master)](https://travis-ci.org/RubenSchmidt/giscademy)

## Quickstart
First create and activate your virtualenv, you can use virtualenvwrapper. Then install the requirements by running:
    
```
$ git clone https://github.com/RubenSchmidt/giscademy.git
$ cd giscademy

# Install the requirements
$ pip install -r requirements.txt

# Perform database migrations
$ python manage.py migrate
```
When everything is set up you can run the development server on localhost:8000 by running:

  ```python manage.py runserver```
  
