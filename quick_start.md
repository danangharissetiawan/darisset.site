# Quick Start Guide

## Download Darisset Blog CMS

First, you need to download the BoilerPlate from GitHub.

## Secret Django Key

This boilerplate has the **DJANGO_KEY** setting variable hidden.

You can generate your DJANGO_KEY [django_key](http://www.miniwebtool.com/django-secret-key-generator"target="_blank").

## Project Name

This project is named _Darisset.site_, so if you are using this
Boilerplate to create your own project, you'll have to change
the name in a few places:

- _darisset.site_ **folder** (your top project container)
- _darisset_site/darisset_ **folder** (your project name)
- virtual environment names: **env** (name them whatever you want)
- create in virtual environments **.env** files (see section below), you have to change **darisset.settings.development** for your **projectname.settings.development**. Same works for the testing environment.

## Virtual environments and Settings Files

First, you must know your Python 3 path::

    $ which python3

which is something similar to /usr/local/bin/python3.

Next, create a Development virtual environment with Python 3 installed::

    $ virtualenv env
    $ source env/bin/activate -> on ubuntu
    $ mkdir .env

You must add the lines:

SECRET_KEY=[..]

EMAIL_HOST=host_your_email
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_email_pasword
EMAIL_PORT=587
DEFAULT_FROM_EMAIL=default_your_email

RECAPTCHA="recaptcha code"

with your project name and your own secret key.

Next, install the packages in each environment::

    $ pip install -r requirements.txt

## Internationalization and Localization

###Settings

The default language for this Project is **English**, and we use internatinalization to translate the text into Indonesia.

If you want to change the translation language, or include a new one, you just need to modify the **LANGUAGES** variable in the file _settings/base.py_. The language codes that define each language can be found [codes_link](<http://msdn.microsoft.com/en-us/library/ms533052(v=vs.85).aspx"target="_blank">).

For example, if you want to use German you should include::

    LANGUAGES = (
        ...
        'id', _("Indonesia"),
        ...
    )

You can also specify a dialect, like Luxembourg's German with::

    LANGUAGES = (
        ...
        'en', _("Engglish"),
        ...
    )

Note: the name inside the translation function \_("") is the language name in the default language (English).

###Translation

Go to the terminal, inside the dariset.site folder and create the files to translate with::

    $ python manage.py makemessages -l id

change the language "id" for your selected language.

Next, go to the locale folder of your language::

    $ cd darisset/locale/ca/LC_MESSAGES

where darisset is your project folder. You have to edit the file _django.po_ and translate the strings.

Once the translation is done, compile your messages with::

    $ python manage.py compilemessages -l id

###Useful commands

A list of all the commands used to run this template::

    $ source env/bin/activate
    $ mkdir .env


    You must add the lines: ::

    SECRET_KEY=[..]

    EMAIL_HOST=host_your_email
    EMAIL_HOST_USER=your_email
    EMAIL_HOST_PASSWORD=your_email_pasword
    EMAIL_PORT=587
    DEFAULT_FROM_EMAIL=default_your_email

    RECAPTCHA="recaptcha code"

    python manage.py createsuperuser

    $ python manage.py runserver

    $ python manage.py makemessages -l id
    $ python manage.py compilemessages -l id
