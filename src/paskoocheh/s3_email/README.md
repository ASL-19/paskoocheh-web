# MANAGING S3_EMAIL DYNAMIC MODELS #

This file documents how to manage dynamic models on the s3_email app

## When deploy is done, you have to start with no dynamic models

### How to get set up with no dynamic models ###

* Open signals.py
* Toggle the ping variable to False
* Run `makemigrations` command
* Run `migrate` command
* Toggle ping back to True in signals.py
* Restart app and celery

### Adding new models ###

* When adding a new emailtype, allow for the page to redirect you after clicking save
* Avoid clicking on links after you click save for the emailtype model until you are redirected
* When adding multiple emailtype objects at a time, celery might get cluttered and not add all the emails
* If multiple celery processes are simultaneously running, make sure all of your emails are added once the processes are done

### How to delete only specific models by making migrations manually ###

* Create the migration manually in s3_email/migrations/filename.py
* Open signals.py and toggle ping to False
* Run `migrate` command
* Toggle ping back to True in signals.py

## How to delete only specific models by making migrations automatically ###

* Open signals.py and toggle ping to False
* Open the created migrations files
* Delete migrations concerning models you do not wish to delete
* Run `migrate` command
* Toggle ping back to True in signals.py
