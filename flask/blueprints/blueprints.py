# -*- coding: utf-8 -*-
"""

"""

from flask import Blueprint, request, render_template, session

from src.models.document import Document
import pickle

# create our blueprint :)
bp = Blueprint('heraldic', __name__)


@bp.route("/")
def hello():
    return render_template('url_form.html')
    # return "<h1 style='color:blue'>Hello There LOL!</h1>"


@bp.route("/gather_document", methods=['POST'])
def gather_document():
    d = Document()
    d.gather(request.form['url'])
    d.extract_fields()
    session['model'] = pickle.dumps(d.model)

    return render_template('url_downloaded.html', model=d.model)

