# -*- coding: utf-8 -*-
"""

"""

from flask import Blueprint, request, render_template

from src.gathering.document_gatherer import DocumentGatherer

# create our blueprint :)
bp = Blueprint('heraldic', __name__)


@bp.route("/")
def hello():
    return render_template('url_form.html')
    # return "<h1 style='color:blue'>Hello There LOL!</h1>"


@bp.route("/gather_document", methods=['POST'])
def gather_document():
    dg = DocumentGatherer(request.form['url'])
    extractor_name = globals()[dg.media_name + 'Extractor']
    extractor = extractor_name(dg.html_content, dg.url)

    return render_template('url_downloaded.html', url=dg.url, domain=dg.domain, media_name=dg.media_name,
                           document_body=extractor.document_body)

