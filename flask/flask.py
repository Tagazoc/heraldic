from flask import Flask
from werkzeug.utils import find_modules, import_string


def create_app(config=None):
    app = Flask('heraldic', template_folder='src/flask/templates', static_folder='src/flask/static')

    app.config.update(dict(
        DEBUG=True,
        SECRET_KEY='IZUAY7CHYzeèzad_ezèyaz'
    ))
    app.config.update(config or {})
    app.config.from_envvar('FLASKR_SETTINGS', silent=True)

    register_blueprints(app)

    return app


def register_blueprints(app):
    """Register all blueprint modules

    Reference: Armin Ronacher, "Flask for Fun and for Profit" PyBay 2016.
    """
    for name in find_modules('src.flask.blueprints'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)
    return None

app = create_app()
