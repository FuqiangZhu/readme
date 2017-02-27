#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *************************************************************************
#   Copyright © 2017 Godinsec. All rights reserved.
#   File Name: __init__.py.py
#   Author: Allan
#   Mail: allan.yan@godinsec.com
#   Created Time: 2017/2/20
# *************************************************************************
from .urls import manage
from app.auth.models import Role, Department


@manage.app_context_processor
def inject_role_and_departmeng():
    return dict(Role=Role, Department=Department)