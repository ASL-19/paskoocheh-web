# -*- coding: utf-8 -*-
# Paskoocheh - A tool marketplace for Iranian
#
# Copyright (C) 2024 ASL19 Organization
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.db.backends.signals import connection_created
from django.urls import clear_url_caches
from django.utils.module_loading import import_module
from paskoocheh.helpers import disable_for_loaddata
from django.core.management import call_command
from django.conf import settings
from boto3.session import Session
from django.contrib import admin
from django.apps import apps
from importlib import reload
import logging


def add_model(sender, connection, **kwargs):
    # get ping from fixtures in the future
    # in order to allow for migrations, toggle ping to False
    # make sure to toggle ping back to True in case it is changed
    ping = True
    logger = logging.getLogger('django')
    logger.setLevel(logging.INFO)
    tables = connection.introspection.table_names()
    changed = False
    app_title = (ping and 's3_email') or (not ping and 'notAnAppName')
    for table in tables:
        if app_title in table:
            _table = table
            name = _table.replace('s3_email_', '')
            logger.info(name)
            if name == 'emailtype':
                continue
            from s3_email.views import make_model
            model = make_model(name)
            if model is None:
                changed = True
                from s3_email.models import BaseEmail, create_Email_model_no_mig
                model = create_Email_model_no_mig(name=str(name),
                                                  fields={'__module__': 's3_email.models'},
                                                  app_label='s3_email',
                                                  admin_opts=BaseEmail
                                                  )
                logger.info(table)
    if changed:
        # SigNumber.objects.get(pk=1).ping += 1
        reload(import_module(settings.ROOT_URLCONF))
        clear_url_caches()

        call_command('makemigrations')
        call_command('migrate')


connection_created.connect(add_model)


def save_meta(sender, instance, **kwargs):
    """
        This function is run on the post_save signal for
        all email objects to update s3 data flags
        ("seen", "deleted", "flag")
    """
    session = Session(region_name=settings.S3_REGION,
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    s3 = session.resource('s3')

    obj = s3.Object(instance.bucket, instance.idTag)
    body = obj.get()['Body'].read()
    seen = 'False'
    flag = 'False'
    deleted = 'False'
    if instance.seen:
        seen = 'True'
    if instance.flag:
        flag = 'True'
    if instance.deleted:
        deleted = 'True'
    obj.put(Metadata={'seen': seen,
                      'deleted': deleted,
                      'flag': flag},
            Body=body)


def save_email(sender, instance, **kwargs):
    """
        gets an instance of emailType with bucket and email fields
        creates new model and retrieves emails corresponding to
        emailType entered
    """
    session = Session(region_name=settings.S3_REGION,
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    s3 = session.resource('s3')
    buck = instance.bucket
    direc = ''
    if '/' in buck:
        direc = buck[buck.index('/') + 1:].replace(' ', '')
        buck = buck[:buck.index('/')]
        if not direc[-1] == '/':
            direc += '/'
    if not s3.Bucket(buck) in s3.buckets.all():
        instance.delete()
        return
    try:
        # testing if bucket is accessible
        for obj in s3.Bucket(buck).objects.all():
            break
    except Exception:
        instance.delete()
        return
    attrs = {
        '__module__': 's3_email.models'
    }
    from s3_email.models import create_Email_model, BaseEmail
    app_models = apps.get_app_config('s3_email').get_models()
    mod = None
    for _model in app_models:
        if _model._meta.model_name == instance.__str__():
            mod = _model
    if mod is None:
        mod = create_Email_model(name=instance.__str__(),
                                 fields=attrs,
                                 app_label='s3_email',
                                 admin_opts=BaseEmail
                                 )
    s3_email_change(sender, instance, **kwargs)


@disable_for_loaddata
def s3_email_change(sender, instance, **kwargs):
    from s3_email.tasks import update_s3_email
    session = Session(region_name=settings.S3_REGION,
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    s3 = session.resource('s3')
    buck = instance.bucket
    direc = ''
    if '/' in buck:
        direc = buck[buck.index('/') + 1:].replace(' ', '')
        buck = buck[:buck.index('/')]
        if not direc[-1] == '/':
            direc += '/'
    if not s3.Bucket(buck) in s3.buckets.all():
        instance.delete()
        return

    reload(import_module(settings.ROOT_URLCONF))
    clear_url_caches()

    app_models = apps.get_app_config('s3_email').get_models()
    model = None
    for _model in app_models:
        if _model._meta.model_name == instance.__str__():
            model = _model
    try:
        from s3_email.models import BaseEmail
        admin.site.register(model, BaseEmail)
    except Exception:
        pass
    update_s3_email(instance.pk, instance.__str__(), direc, buck)
