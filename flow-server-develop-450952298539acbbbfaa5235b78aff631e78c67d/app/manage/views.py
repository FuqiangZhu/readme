#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *************************************************************************
#   Copyright © 2016 Godinsec. All rights reserved.
#   File Name: views.py
#   Author: Allan
#   Mail: allan.yan@godinsec.com
#   Created Time: 16/9/23
# *************************************************************************
import datetime

from flask import current_app, jsonify
from flask import flash
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user, login_required
from werkzeug.utils import redirect

from app import db
from app.auth.models import AdminUser, AdminLog
from app.helper import send_mail, add_admin_log
from app.manage.forms import CreateAdminUserForm, AdminLogForm


@login_required
def list_admin_user():
    page = request.args.get('page', 1, type=int)
    pagination = AdminUser.query.order_by(AdminUser.id.asc()).\
        paginate(page, per_page=current_app.config['RECORDS_PER_PAGE'], error_out=False)
    users = pagination.items
    add_admin_log(user=current_user.username, actions='查询用户', client_ip=request.remote_addr, results='成功')
    return render_template("manage/admin_user.html", users=users, pagination=pagination, action="LIST")


@login_required
def add_admin_user():
    form = CreateAdminUserForm()
    if form.validate_on_submit():
        user = AdminUser()
        user.username = form.username.data
        user.email = form.email.data
        user.role = form.user_type.data
        user.department = form.user_department.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirm_token()
        send_mail([user.email], 'Confirm your account', 'auth/email/confirm', user=user, token=token)
        add_admin_log(user=current_user.username, actions='添加用户', client_ip=request.remote_addr, results='成功')
        return redirect(url_for('manage.list_admin_user'))
    flag = False
    for field, error in form.errors.items():
        if not flag:
            flash(error[0])
            flag = True
    return render_template("manage/admin_user.html", form=form, action="ADD")


@login_required
def del_admin_user():
    AdminUser.query.filter_by(id=request.args.get('id', type=int)).delete()
    db.session.commit()
    add_admin_log(user=current_user.username, actions='删除用户', client_ip=request.remote_addr, results='成功')
    return jsonify(code=0)


@login_required
def set_admin_user_status():
    user = AdminUser.query.filter_by(id=request.args.get('id', type=int)).first()
    if user is not None:
        user.forbidden = not user.forbidden
        db.session.add(user)
        db.session.commit()
        action = '禁止用户'
        if user.forbidden:
            action = '启用用户'
        add_admin_log(user=current_user.username, actions=action, client_ip=request.remote_addr, results='成功')
    return jsonify(code=0)


@login_required
def audit_user():
    form = AdminLogForm()
    query = AdminLog.query
    if form.validate_on_submit():
        username = form.username.data
        actions = form.actions.data
        client_ip = form.client_ip.data
        start_time = form.start_time.data
        end_time = form.end_time.data
    else:
        username = request.args.get('username')
        actions = request.args.get('actions')
        client_ip = request.args.get('client_ip')
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        if start_time is not None and end_time is not None:
            start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    if username is not None:
        form.username.data = username
        if form.username.data != 'all':
            query = query.filter_by(username=form.username.data)
    if actions is not None:
        form.actions.data = actions
        if form.actions.data != 'all':
            query = query.filter_by(actions=form.actions.data)
    if client_ip is not None:
        form.client_ip.data = client_ip
        if form.client_ip.data != 'all':
            query = query.filter_by(client_ip=form.client_ip.data)
    if start_time is not None and end_time is not None:
        form.start_time.data = start_time
        form.end_time.data = end_time
        query = query.filter(AdminLog.log_time.between(form.start_time.data, form.end_time.data))
    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page, per_page=current_app.config['RECORDS_PER_PAGE'], error_out=False)
    logs = pagination.items
    flag = False
    for field, error in form.errors.items():
        if not flag:
            flash(error[0])
            flag = True
            add_admin_log(user=current_user.username, actions='查询日志', client_ip=request.remote_addr, results=error[0])
    if not form.errors:
        add_admin_log(user=current_user.username, actions='查询日志', client_ip=request.remote_addr, results='成功')
    return render_template("manage/audit_user.html", form=form, logs=logs, pagination=pagination)


@login_required
def export_result():
    export_type = request.args.get('export_type', type=int)
    if export_type == 1:
        pass
    elif export_type == 2:
        pass
    else:
        pass


def get_week_day_range():
    year = request.args.get('year', type=int)
    week = request.args.get('week', type=int)
    basic_day = datetime.date(year=year, month=12, day=31)
    basic_week = basic_day.isocalendar()[1]
    week_first_day = basic_day - datetime.timedelta(days=basic_day.weekday()) - datetime. \
        timedelta(days=(basic_week - week) * 7)
    week_last_day = week_first_day + datetime.timedelta(days=6)
    data = week_first_day.strftime("%Y-%m-%d") + '--' + week_last_day.strftime("%Y-%m-%d")
    return jsonify(code=0, data=data)

