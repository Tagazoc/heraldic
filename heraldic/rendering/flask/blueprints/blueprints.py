# -*- coding: utf-8 -*-
"""

"""

from flask import Blueprint, request, render_template, flash, redirect, url_for, abort
from flask_nav.elements import Navbar, View

from heraldic.misc.exceptions import DocumentNotChangedException
from heraldic.models.document import Document
from heraldic.rendering.flask.forms import UrlForm, ReviewForm, DisplayDocumentForm
from heraldic.rendering.flask.nav import nav
from heraldic.media.known_media import known_media
from heraldic.store import index_searcher


bp = Blueprint('heraldicapp', __name__)

nav.register_element('heraldic_top', Navbar(
    View('Liste', '.home'),
    View('Soumettre un article', '.submit_document')
))


@bp.route("/", methods=['GET'])
def home():
    media_classes = known_media.media_classes
    return render_template('home.html', media_classes=media_classes)


@bp.route('/display_media', methods=['GET'])
def display_media():
    media_id = request.args.get('media_id')
    if not known_media.media_exists(media_id):
        abort(401)
    hits_generator = index_searcher.search_by_media(media_id)
    hits_models = [next(hits_generator) for _ in range(100)]
    return render_template('search.html', hits=hits_models)


@bp.route('/display_document', methods=['GET', 'POST'])
def display_document():
    doc_id = request.args.get('doc_id')

    d = Document(doc_id=doc_id)
    d.retrieve_old_versions()

    form = DisplayDocumentForm(data={'id': d.model.id.value})

    return render_template('display_document.html', document=d, form=form)


@bp.route('/submit_document', methods=['GET', 'POST'])
def submit_document():
    form = UrlForm()

    if form.validate_on_submit():
        url = form.url.data

        d = Document(url)
        if d.model.initialized:
            flash("L'article existe déjà", "warning")
        else:
            d.gather()
            flash("L'article a été récupéré", "info")

        return redirect(url_for('heraldicapp.review_document', id=d.model.id))

    return render_template('url_form.html', form=form)


@bp.route("/review_document", methods=['GET', 'POST'])
def review_document():
    doc_id = request.form['id'] if request.method == 'POST' else request.args['id']
    d = Document(doc_id=doc_id)

    ReviewForm.apply_model(d.model)
    form = ReviewForm()

    if form.validate_on_submit():
        if 'gather_again' in request.form:
            try:
                d.gather(force_update=True)
                flash("L'article a de nouveau été récupéré", "info")
            except DocumentNotChangedException:
                flash("Aucune mise à jour constatée", "danger")
        else:
            try:
                d.update_from_revision(request.form)
                flash("L'article a été mis à jour", "info")
            except DocumentNotChangedException:
                flash("Aucune mise à jour constatée", "danger")

    form.apply_model_default_values(d.model)

    form.process()
    return render_template('review_document.html', form=form)


@bp.route("/regather_document", methods=['GET'])
def regather_document():
    doc_id = request.args['id']
    d = Document(doc_id=doc_id)
    try:
        d.gather(force_update=True)
    except DocumentNotChangedException:
        flash("Aucune mise à jour constatée", "danger")
    d.retrieve_old_versions()

    form = DisplayDocumentForm(data={'id': d.model.id.value})

    return render_template('display_document.html', document=d, form=form)

