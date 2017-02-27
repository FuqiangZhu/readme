#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *************************************************************************
#   Copyright © 2016 Godinsec. All rights reserved.
#   File Name: helper.py
#   Author: Allan
#   Mail: allan.yan@godinsec.com
#   Created Time: 16/9/27
# *************************************************************************
import os
from datetime import datetime
from threading import Thread

from flask import render_template, current_app
from flask_mail import Message

from . import mail, db
from .auth.models import AdminLog


def send_mail(to, subject, template, attachments=None, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject,
                  recipients=to, sender=app.config['MAIL_SENDER'])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    if attachments is not None:
        for attachment in attachments:
            file_name = os.path.basename(attachment)
            with app.open_resource(attachment) as fp:
                msg.attach(file_name, content_type='text/plain', data=fp.read())

    def send_mail_async(message):
        with app.app_context():
            mail.send(message)

    thr = Thread(target=send_mail_async, args=[msg])
    thr.start()


def add_admin_log(user, actions, client_ip, results):
    log = AdminLog()
    log.username = user
    log.actions = actions
    log.client_ip = client_ip
    log.results = results
    db.session.add(log)
    db.session.commit()


def print_log(action, function, branch, api_version, imei=None):
    log_msg = '***** ' + action + ' ' + function + '@' + branch + '@api_' + \
              api_version
    if imei is not None:
        log_msg += '-' + imei + '-'
    log_msg += '@' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' *****'
    print(log_msg)
