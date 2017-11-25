#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class used as a model for documents.
"""

from flask_wtf import FlaskForm
from wtforms.fields import *
from src.models.document_model import DocumentModel
from src.models.attribute import *


class UrlForm(FlaskForm):
    url = StringField("URL de l'article")

    submit = SubmitField(u'Soumettre')


class ReviewForm(FlaskForm):
    @classmethod
    def apply_model(cls, model: DocumentModel):
        for k, v in model.attributes.items():
            if not v.displayable:
                continue
            field_class = Attribute
            kwargs = {'label': v.desc}
            if isinstance(v, StringAttribute) or isinstance(v, DateAttribute):
                field_class = StringField
            elif isinstance(v, StringListAttribute):
                field_class = TextAreaField
            elif isinstance(v, BooleanAttribute):
                field_class = SelectField
                kwargs['choices'] = [('yes', 'Oui'), ('no', 'Non')]
            kwargs['default'] = v.render()
            setattr(cls, k, field_class(**kwargs))

            setattr(cls, 'submit', SubmitField('Corriger'))
