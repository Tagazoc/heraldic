# -*- coding: utf-8 -*-
"""

"""

from flask import Blueprint, request, render_template, session, url_for, flash
from flask_nav.elements import Navbar, View
from src.rendering.flask.nav import nav
from src.rendering.flask.elasticsearch import es
from src.rendering.flask.forms import UrlForm, ReviewForm
from src.models.document import Document
from src.store.model_searcher import ModelSearcher


# create our blueprint :)
bp = Blueprint('heraldic', __name__)

nav.register_element('heraldic_top', Navbar(
    View('Liste', '.home'),
    View('Soumettre un article', '.submit_document')
))


@bp.route("/", methods=['GET'])
def home():
    ms = ModelSearcher(es)
    ms.search_all_docs()
    return render_template('search.html', hits=ms.hits_models)


@bp.route('/submit_document', methods=['GET', 'POST'])
def submit_document():
    form = UrlForm()

    if form.validate_on_submit():
        url = request.form['url']
        d = Document(es)

        d.retrieve_from_url(url)
        if d.model.id.value:
            flash("L'article existe déjà")
        else:
            d.gather(url)
            d.extract_fields()

            d.store()
            flash("L'article a été récupéré")
        ReviewForm.apply_model(d.model)
        review_form = ReviewForm()

        review_form.process()
        return render_template('review_document.html', form=review_form)

    return render_template('url_form.html', form=form)


@bp.route("/review_document", methods=['POST'])
def review_document():
    d = Document(es)
    d.retrieve(request.form['id'])

    d.update_from_display(request.form)

    ReviewForm.apply_model(d.model)
    form = ReviewForm()

    form.process()
    flash("L'article a été mis à jour")
    return render_template('review_document.html', form=form)
