#!/bin/bash
################################## OBSOLETE ##################################

# Runs Celery worker and Celery beat (for development only)
celery worker --beat --app paskoocheh --loglevel INFO --logfile logs/celery.log
