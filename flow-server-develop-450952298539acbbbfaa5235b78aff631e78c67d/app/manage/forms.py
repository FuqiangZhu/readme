#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *************************************************************************
#   Copyright © 2016 Godinsec. All rights reserved.
#   File Name: forms.py
#   Author: Allan
#   Mail: allan.yan@godinsec.com
#   Created Time: 16/9/27
# *************************************************************************
from flask_wtf import Form
from wtforms import SelectField, StringField, PasswordField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, Email, ValidationError, Optional
from app import db
from app.auth.models import Role, AdminUser, Department, AdminLog


class CreateAdminUserForm(Form):
    user_type = SelectField('用户类型', validators=[DataRequired(message='请选择用户类型')], coerce=int,
                            choices=[(Role.ADMIN, '管理员'), (Role.AUDITOR, '审计员'), (Role.USER, '一般用户')])
    user_department = SelectField('用户部门', validators=[DataRequired(message='请选择用户部门')], coerce=int,
                                  choices=[(Department.PM, '项目经理'), (Department.OPERATION, '运营部'),
                                           (Department.PRODUCTION, '产品部'), (Department.QA, '测试部'),
                                           (Department.DEVELOP, '研发部'), (Department.DEVELOP_SU, '研发部-开发者')])
    username = StringField('用户名', validators=[DataRequired(message='用户名不能为空'),
                                              Length(4, 20, message='用户名长度必须在4-20之间'),
                                              Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户名包含非法字符')])
    email = StringField('邮箱', validators=[DataRequired(message='邮箱不能为空'), Email(message='邮箱格式错误')])
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空'),
                                               Length(8, 30, message='密码长度必须在8-30之间')])
    password2 = PasswordField('确认密码', validators=[DataRequired(message='确认密码不能为空'),
                                                  Length(8, 30, message='确认密码长度必须在8-30之间'),
                                                  EqualTo('password', message='两次密码输入不一致')])
    submit = SubmitField('添加')

    def validate_username(self, field):
        if AdminUser.query.filter_by(username=field.data).first() is not None:
            raise ValidationError('用户名已存在')

    def validate_email(self, field):
        if AdminUser.query.filter_by(email=field.data).first() is not None:
            raise ValidationError('邮箱已使用')


class AdminLogForm(Form):
    username_choice = [('all', '全部')] + \
                      [(username[0], username[0]) for username in db.session.query(AdminLog.username.distinct())]

    actions_choice = [('all', '全部')] + \
                     [(action[0], action[0]) for action in db.session.query(AdminLog.actions.distinct())]

    ip_choice = [('all', '全部')] + \
                [(ip[0], ip[0]) for ip in db.session.query(AdminLog.client_ip.distinct())]

    username = SelectField('用户名', choices=username_choice, default='all')
    actions = SelectField('操作', choices=actions_choice, default='all')
    client_ip = SelectField('登陆地址', choices=ip_choice, default='all')
    start_time = DateTimeField('起始时间', validators=[Optional()])
    end_time = DateTimeField('终止时间', validators=[Optional()])
    submit = SubmitField('查询')

    def validate_start_time(self, field):
        if field.data is not None and self.end_time.data is None:
            raise ValidationError('终止时间不能为空')

    def validate_end_time(self, field):
        if field.data is not None and self.start_time.data is None:
            raise ValidationError('起始时间不能为空')
        if field.data is not None and self.start_time.data is not None and \
                (self.start_time.data > field.data):
            raise ValidationError('终止时间不能小于起始时间')
