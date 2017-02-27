#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *************************************************************************
#   Copyright © 2016 Godinsec. All rights reserved.
#   File Name: config.py
#   Author: Allan
#   Mail: allan.yan@godinsec.com
#   Created Time: 16/9/21
# *************************************************************************


class Config(object):

    SECRET_KEY = 'godinsec'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 通知邮件配置
    MAIL_SERVER = 'smtp.mxhichina.com'
    MAIL_PORT = 25
    MAIL_USERNAME = 'sys_report@godinsec.com'
    MAIL_PASSWORD = 'Godinsec@123!'
    MAIL_SENDER = 'Admin <sys_report@godinsec.com>'

    RECORDS_PER_PAGE = 10
    RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
    RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'

    def __repr__(self):
        return '<Config>'


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://godin_root:Godinsec2016@rm-2zezrr3ffz4stu7de.mysql.rds.aliyuncs.com/flow'
    SERVER_ADDRESS = '0.0.0.0'
    SERVER_PORT = 9020
    QR_CODE_IMAGE = 'qr_code_product.png'
    MAIL_SUBJECT_PREFIX = '流量充值生产环境'

    def __repr__(self):
        return '<ProductionConfig>'


class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:sa@127.0.0.1/flow'
    SERVER_ADDRESS = '0.0.0.0'
    SERVER_PORT = 9020
    QR_CODE_IMAGE = 'qr_code_test.png'
    MAIL_SUBJECT_PREFIX = '流量充值外网测试环境'

    def __repr__(self):
        return '<TestConfig>'


class InternalTestConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:sa@10.0.4.253/flow'
    SERVER_ADDRESS = '0.0.0.0'
    SERVER_PORT = 9020
    QR_CODE_IMAGE = 'qr_code_internal_test.png'
    MAIL_SUBJECT_PREFIX = '流量充值内网测试环境'

    def __repr__(self):
        return '<InternalTestConfig>'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:sa@127.0.0.1/flow'
    SERVER_ADDRESS = '127.0.0.1'
    SERVER_PORT = 9020
    QR_CODE_IMAGE = 'qr_code_develop.png'
    MAIL_SUBJECT_PREFIX = '流量充值开发环境'

    def __repr__(self):
        return '<DevelopmentConfig>'

config = {'development': DevelopmentConfig,
          'test': TestConfig,
          'internal': InternalTestConfig,
          'production': ProductionConfig,

          'default': DevelopmentConfig}
