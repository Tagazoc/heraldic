
from flask import Blueprint, request, render_template, flash, redirect, url_for, abort
from flask_nav.elements import Navbar, View

from heraldic.misc.exceptions import DocumentNotChangedException
from heraldic.models.document import Document
from heraldic.rendering.flask.forms import UrlForm, ReviewForm, DisplayDocumentForm
from heraldic.rendering.flask.nav import nav
from heraldic.media.known_media import known_media
from heraldic.store import index_searcher


bp = Blueprint('heraldicapi', __name__)


