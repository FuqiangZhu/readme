#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *************************************************************************
#   Copyright © 2016 Godinsec. All rights reserved.
#   File Name: urls.py
#   Author: Allan
#   Mail: allan.yan@godinsec.com
#   Created Time: 16/9/23
# *************************************************************************
from .views import list_admin_user, add_admin_user, del_admin_user, set_admin_user_status, audit_user
from flask import Blueprint

manage = Blueprint('manage', __name__, static_folder='static', template_folder='templates')

manage.add_url_rule('/list_admin_user', view_func=list_admin_user)
manage.add_url_rule('/add_admin_user', view_func=add_admin_user, methods=['GET', 'POST'])
manage.add_url_rule('/del_admin_user', view_func=del_admin_user)
manage.add_url_rule('/set_admin_user_status', view_func=set_admin_user_status)
manage.add_url_rule('/audit_user', view_func=audit_user, methods=['GET', 'POST'])