#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module which runs an API
"""

import connexion


def create_app():
    app = connexion.App('heraldicapi', specification_dir='heraldic/rendering/flask/api/')

    app.add_api('swagger.yml')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
