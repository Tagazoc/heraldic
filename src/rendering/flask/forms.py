#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Class used as a model for documents.
"""

from flask_wtf import FlaskForm, Form
from wtforms.fields import *
from src.models.document_model import DocumentModel
from src.models.attribute import *
from wtforms.validators import ValidationError


class UrlForm(FlaskForm):
    url = StringField("URL de l'article")
    gather_again = HiddenField()

    submit = SubmitField(u'Soumettre')


class ReviewForm(FlaskForm):
    @classmethod
    def apply_model(cls, model: DocumentModel):
        for k, v in model.attributes.items():
            if not v.displayable:
                continue
            field_class = Attribute
            kwargs = {'label': v.desc}
            if k == 'id':
                field_class = HiddenField
            elif isinstance(v, StringAttribute) or isinstance(v, DateAttribute):
                field_class = StringField
            elif isinstance(v, StringListAttribute):
                field_class = TextAreaField
            elif isinstance(v, BooleanAttribute):
                field_class = SelectField
                kwargs['choices'] = [('yes', 'Oui'), ('no', 'Non')]

                # Add default parameter first for handling WTForms issue #289
                kwargs['default'] = 'no'

            if not v.revisable and k != 'id':
                kwargs['render_kw'] = {'disabled': 'disabled'}
            if v.revisable:
                kwargs['validators'] = [cls.generate_validator(v)]
            setattr(cls, k, field_class(**kwargs))

        setattr(cls, 'submit', SubmitField('Corriger'))
        setattr(cls, 'gather_again', SubmitField('Récupérer à nouveau'))

    def apply_model_default_values(self, model: DocumentModel):
        for k, v in model.attributes.items():
            if not v.displayable:
                continue
            getattr(self, k).default = v.render_for_display()

    @classmethod
    def generate_validator(cls, attribute):
        def validator(form, field):
            if not attribute.validate(field.data):
                raise ValidationError(attribute.validate_failure_text)

        return validator


class DisplayDocumentForm(FlaskForm):
    id = HiddenField()

    submit = SubmitField(u'Mettre à jour l\'article')
