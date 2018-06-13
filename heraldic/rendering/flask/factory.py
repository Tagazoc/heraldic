#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class used as a model for documents.
"""

from flask import Flask
from flask_bootstrap import Bootstrap
from heraldic.rendering.flask.nav import nav
from werkzeug.utils import find_modules, import_string


def create_app(config=None):
    app = Flask('heraldicapp', template_folder='heraldic/rendering/flask/templates', static_folder='heraldic/rendering/flask/static')

    app.config.update(dict(
        DEBUG=True,
        SECRET_KEY='IZUAY7CHYzeèzad_ezèyaz'
    ))

    app.config.update(config or {})

    app.config.from_envvar('FLASKR_SETTINGS', silent=True)

    Bootstrap(app)
    register_blueprints(app)

    nav.init_app(app)

    return app


def register_blueprints(app):
    """Register all blueprint modules

    Reference: Armin Ronacher, "Flask for Fun and for Profit" PyBay 2016.
    """
    for name in find_modules('heraldic.rendering.flask.blueprints'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)
    return None
