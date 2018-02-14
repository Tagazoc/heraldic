# -*- coding: utf-8 -*-
"""

"""

from flask import Blueprint, request, render_template, flash
from flask_nav.elements import Navbar, View

from src.heraldic_exceptions import DocumentNotFoundException
from src.models.document import Document
from src.rendering.flask.forms import UrlForm, ReviewForm
from src.rendering.flask.nav import nav
from src.store import model_searcher

bp = Blueprint('heraldic', __name__)

nav.register_element('heraldic_top', Navbar(
    View('Liste', '.home'),
    View('Soumettre un article', '.submit_document')
))


@bp.route("/", methods=['GET'])
def home():
    hits_models = model_searcher.search_all_docs()
    return render_template('search.html', hits=hits_models)


@bp.route('/display_document', methods=['GET', 'POST'])
def display_document():
    doc_id = request.args.get('doc_id')

    d = Document()
    d.retrieve(doc_id)
    d.retrieve_old_versions(doc_id)

    return render_template('display_document.html', document=d)


@bp.route('/submit_document', methods=['GET', 'POST'])
def submit_document():
    form = UrlForm()

    if form.validate_on_submit():
        url = form.url.data  # request.form['url']
        d = Document()

        try:
            d.retrieve_from_url(url)
        except DocumentNotFoundException:
            d.gather(url)
            d.extract_fields()

            d.store()
            flash("L'article a été récupéré", "info")
        else:
            flash("L'article existe déjà", "warning")

        ReviewForm.apply_model(d.model)
        review_form = ReviewForm()
        review_form.process()

        return render_template('review_document.html', form=review_form)

    return render_template('url_form.html', form=form)


@bp.route("/review_document", methods=['POST'])
def review_document():
    d = Document()
    d.retrieve(request.form['id'])

    if 'gather_again' in request.form:
        new_d = Document()
        new_d.gather(d.model.url)
        new_d.extract_fields()
        d.update_from_model(new_d.model)
        flash("L'article a de nouveau été récupéré", "info")

    else:

        d.update_from_display(request.form)
        flash("L'article a été mis à jour", "info")

    ReviewForm.apply_model(d.model)
    form = ReviewForm()

    form.process()
    return render_template('review_document.html', form=form)
