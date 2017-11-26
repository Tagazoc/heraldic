# -*- coding: utf-8 -*-
"""

"""

from flask import Blueprint, request, render_template, session, url_for, flash
from flask_nav.elements import Navbar, View
from src.rendering.flask.nav import nav

from src.models.document import Document
from src.rendering.flask.forms import UrlForm, ReviewForm

# create our blueprint :)
bp = Blueprint('heraldic', __name__)

nav.register_element('heraldic_top', Navbar(
    View('Home', '.home')
))


@bp.route("/", methods=['GET', 'POST'])
def home():
    form = UrlForm()

    if form.validate_on_submit():
        d = Document()
        d.gather(request.form['url'])
        d.extract_fields()

        d.store()
        flash("L'article a été récupéré")
        ReviewForm.apply_model(d.model)
        review_form = ReviewForm()

        review_form.process()
        return render_template('url_downloaded.html', form=review_form)

    return render_template('url_form.html', form=form)


@bp.route("/review_document", methods=['POST'])
def review_document():
    d = Document()
    d.retrieve(request.form['id'])
    for k, v in d.model.attributes.items():
        if v.revisable:
            v.update_from_display(request.form[k])

    d.update()
    ReviewForm.apply_model(d.model)
    form = ReviewForm()

    form.process()
    flash("L'article a été mis à jour")
    return render_template('url_downloaded.html', form=form)
