#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *************************************************************************
#   Copyright © 2017 Godinsec. All rights reserved.
#   File Name: __init__.py.py
#   Author: Allan
#   Mail: allan.yan@godinsec.com
#   Created Time: 2017/2/20
# *************************************************************************
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_moment import Moment
from flask_wtf import CsrfProtect
from flask_cache import Cache

from .config.config import config

bootstrap = Bootstrap()
page_down = PageDown()
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
moment = Moment()
cache = Cache()
csrf = CsrfProtect()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    bootstrap.init_app(app)
    page_down.init_app(app)
    db.init_app(app)
    db.app = app
    mail.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    cache.init_app(app)
    app.jinja_env.add_extension('jinja2.ext.do')

    from .manage.urls import manage as manage_blueprint
    app.register_blueprint(manage_blueprint, url_prefix='/flow/manage')

    from .auth.urls import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/flow/auth')

    return app
