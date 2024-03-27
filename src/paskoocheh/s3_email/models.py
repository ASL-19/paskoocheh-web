# -*- coding: utf-8 -*-
# Paskoocheh - A tool marketplace for the Iranian
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
from __future__ import unicode_literals

from s3_email.signals import save_meta, save_email
from django.contrib.postgres.fields import ArrayField
from django.urls import clear_url_caches
from django.utils.module_loading import import_module
from django.core.management import call_command
from django.db.models.signals import post_save
from django.http import HttpResponseRedirect
from django.conf import settings
from markdownify import markdownify as md
from email.header import decode_header
from boto3.session import Session
from django.contrib import admin
from django.db import models
from importlib import reload
import email as em
import datetime
import logging
# import sys
import re


class EmailType(models.Model):
    """
        Emails sent to admin@paskoocheh.com are declared
        of this object type
    """
    from s3_email.validators import validate_buck
    email = models.CharField(max_length=20, default="",
                             blank=True)
    bucket = models.CharField(max_length=40, default="",
                              blank=True, validators=[validate_buck])

    def __str__(self):
        emailstr = re.sub(r"\W+", "", self.email.lower())
        return str(emailstr)

    class Meta:
        unique_together = ('bucket', 'email')


post_save.connect(save_email, sender=EmailType)


def create_Email_model(name, fields=None, app_label='', admin_opts=None, module='',
                       options=None):
    """
        Create specified model
    """

    class Meta:
        verbose_name_plural = name
    if app_label:
        setattr(Meta, 'app_label', app_label)
    if options is not None:
        for key, value in options.iteritems():
            setattr(Meta, key, value)
    attrs = {'__module__': module, 'Meta': Meta}
    if fields:
        attrs.update(fields)

    model = type(name, (Email,), attrs)
    if admin_opts is not None:
        admin.site.register(model, admin_opts)
        reload(import_module(settings.ROOT_URLCONF))
        clear_url_caches()

        call_command('makemigrations')
        call_command('migrate')

        post_save.connect(save_meta, sender=model)
    return model


def create_Email_model_no_mig(name, fields=None, app_label='', admin_opts=None, module='',
                              options=None):
    """
        Create specified model
    """

    class Meta:
        verbose_name_plural = name
    if app_label:
        setattr(Meta, 'app_label', app_label)
    if options is not None:
        for key, value in options.iteritems():
            setattr(Meta, key, value)
    attrs = {'__module__': module, 'Meta': Meta}
    if fields:
        attrs.update(fields)

    model = type(name, (Email,), attrs)
    if admin_opts is not None:
        admin.site.register(model, admin_opts)

        post_save.connect(save_meta, sender=model)
    return model


class Email(models.Model):
    """
        Parent abstract Email model
        child models inherit from Email
    """

    seen = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    flag = models.BooleanField(default=False)
    idTag = models.CharField(max_length=255, blank=True,
                             null=False, default="", primary_key=True)
    date = models.DateField(blank=True, null=True,
                            default=datetime.date.today)
    subject = models.CharField(max_length=512,
                               blank=True, null=True,
                               default="")
    body = models.TextField(blank=True, null=True,
                            default="")
    sender = models.CharField(max_length=512,
                              blank=True, null=True,
                              default="")
    recipients = ArrayField(models.CharField(max_length=512,
                                             default=""),
                            blank=True, null=True)
    bucket = models.CharField(max_length=40, default="",
                              blank=True)
    ccList = ArrayField(models.CharField(max_length=512,
                                         default=""),
                        blank=True, null=True)
    emailType = models.ForeignKey(EmailType, default=None,
                                  null=True,
                                  on_delete=models.SET_NULL)

    def __str__(self):
        return '%s' % (self.subject)

    class Meta:
        unique_together = ('idTag', 'date',)
        abstract = True


post_save.connect(save_meta, sender=Email)


class BaseEmail(admin.ModelAdmin):
    """
        Similar variables are displayed for all email objects despite
        different object types (child models)
    """

    # change_list_template = 'admin/s3_email/change_list.html'
    search_fields = [
        'idTag',
        'date',
        'subject',
        'body',
        'sender',
        'recipients',
        'ccList',
        'bucket']
    list_display = (
        'subject',
        'date',
        'sender',
        'bucket',
        'seen',
        'flag')
    fields = (
        'seen',
        'flag',
        'deleted',
        'idTag',
        'date',
        'subject',
        'body',
        'sender',
        'recipients',
        'ccList',
        'bucket')


def get_email_body(email_obj):
    bodyLns = ''
    if email_obj.is_multipart():
        for payload in email_obj.get_payload():
            if not payload.is_multipart():
                bodyLns += payload.get_payload()
            else:
                for _payload in payload.get_payload():
                    if not _payload.is_multipart():
                        bodyLns += _payload.get_payload()
    else:
        bodyLns = email_obj.get_payload()
    return bodyLns


def s3_email(idno, email, direc, buck):
    """
        Updates the admin page email list by retrieving data from s3
        Also sets "flag", "deleted" and "seen" flags to "False"
        if flags do not already exist for any s3 data entries
    """
    from datetime import datetime
    logger = logging.getLogger('django')
    logger.setLevel(logging.INFO)
    from s3_email.views import make_model, parse_email
    model = make_model(email)
    if model is None:
        model = create_Email_model(name=str(email),
                                   fields={'__module__': 's3_email.models'},
                                   app_label='s3_email',
                                   admin_opts=BaseEmail
                                   )
    emailType = EmailType.objects.get(pk=idno)
    bucketName = buck
    session = Session(region_name=settings.S3_REGION,
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    s3 = session.resource('s3')
    bucket = s3.Bucket(bucketName)
    ccList = []

    logger.info("DIRECTORY: " + direc)

    for obj in bucket.objects.all():
        if not obj.key.startswith(direc) or '.' in obj.key or not len(obj.key) == 40 + len(direc):
            continue
        bod = obj.get()['Body'].read()
        email_obj = em.message_from_string(bod)

        bodyLns = get_email_body(email_obj)
        dateLn = str(email_obj['Date'])
        fromLn = str(email_obj['From'])
        toLn = str(email_obj['To'])
        if email.lower() not in toLn.lower():
            continue
        subjectLn = email_obj['Subject']
        encoding = email_obj['Content-Transfer-Encoding']
        ccStringLn = parse_email(obj.get()['Body'].read())
        if not dateLn == '':
            dateLn = datetime.strptime(dateLn[:-6], '%a, %d %b %Y %X')
        else:
            dateLn = datetime.now()
        if ccStringLn is not None:
            ccStringLn = ccStringLn.replace("Cc: ", "")
            ccList = ccStringLn.split(', ')
        create_obj(dateLn, fromLn, toLn, subjectLn, bodyLns,
                   ccList, obj, bucketName, emailType, model, encoding)
        logger.info(obj.key)
    logger.info('done s3_email')
    HttpResponseRedirect('/admin/s3_email/')


def parse_subject(subjectLn):
    sub = ''
    for word in subjectLn.split():
        if '=?UTF-8?B?' in word or '=?=' in word:
            word = word.replace('=?UTF-8?B?', '').replace('=?=', '')
            missing_padding = len(word) % 4
            if missing_padding != 0:
                word += b'=' * (4 - missing_padding)
            try:
                word = word.encode('utf-8')
            except Exception:
                pass
            try:
                sub += word.decode('base64')
            except Exception:
                sub += word
        else:
            sub += word + ' '
    return sub


def parse_body(bodyLns, encoding):
    bod = ''
    for word in bodyLns.split():
        if not encoding == 'utf8':
            word = word.encode('utf-8')
            try:
                bod += word.decode(encoding)
            except Exception:
                try:
                    bod += str(word.decode(encoding), errors='ignore')
                except Exception:
                    bod += word
        else:
            bod += word + ' '
    bod = bod.replace('<br>', '\n')
    bod = md(bod)
    return bod


def create_obj(dateLn, fromLn, toLn, subjectLn, bodyLns, CCList, obj, bucketName, newType, model, encoding):
    """
        Creating email objects
    """
    dh = decode_header(subjectLn)
    default_charset = 'ASCII'
    try:
        sub = ''.join([str(t[0], t[1] or default_charset) for t in dh])
    except Exception:
        sub = parse_subject(subjectLn)
    bod = parse_body(bodyLns, encoding)

    try:
        newEmail = model(idTag=obj.key,
                         date=dateLn,
                         subject=sub,
                         body=bod,
                         sender=fromLn,
                         recipients=[toLn],
                         ccList=CCList,
                         bucket=bucketName,
                         emailType=newType
                         )
    except Exception:
        newEmail = model(idTag=obj.key,
                         date=dateLn,
                         subject=subjectLn,
                         body=bodyLns,
                         sender=fromLn,
                         recipients=[toLn],
                         ccList=CCList,
                         bucket=bucketName,
                         emailType=newType
                         )

    newEmail.save()
    body = obj.get()['Body'].read()
    if ("seen" not in obj.get()['Metadata'].keys() or "deleted" not in obj.get()['Metadata'].keys() or "flag" not in obj.get()['Metadata'].keys()):
        obj.put(Metadata={'seen': 'False',
                          'deleted': 'False',
                          'flag': 'False'},
                Body=body)
