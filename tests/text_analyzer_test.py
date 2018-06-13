#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Text analyzer test module.
"""

from heraldic.analysis.text_analyzer import TextAnalyzer
import pytest


@pytest.fixture
def text():
    return 'Les grillons se sont tus mais l’odeur des pins reste entêtante. La nuit tombe doucement, enveloppant la ' \
           'colline boisée de la Pnyx qui domine Athènes, en face de l’Acropole éclairée. Léger, le vent fait danser ' \
           'les feuilles des oliviers, derrière le pupitre blanc. L’image est belle, spectaculaire. Emmanuel Macron – ' \
           'qui, en la matière, n’a jamais peur d’en faire trop – l’avait soignée, dans les pas d’André Malraux, ' \
           'qui avait discouru là voici près de soixante ans. En visite d’Etat pendant deux jours en Grèce, ' \
           'jeudi 7 et vendredi 8 septembre, le président de la République avait choisi cette colline, berceau de la ' \
           'démocratie athénienne, où l’assemblée des citoyens votait les décisions de la cité à main levée, ' \
           'pour lancer son appel à refonder l’Europe. « Ces lieux nous obligent », a-t-il commencé après quelques ' \
           'mots prononcés en grec devant un parterre d’invités, dont des lycéens. « C’est ici que fut inventée la ' \
           'forme moderne de l’Etat, ici que cette cité d’Athènes construisit patiemment, par la souveraineté du ' \
           'peuple, la souveraineté de son destin », a-t-il ajouté avant d’interroger : « Qu’avons-nous fait, nous, ' \
           'Européens, de notre souveraineté ? (…) Qu’avons-nous fait de la démocratie ? Nous faisons-nous encore ' \
           'confiance ? (…) En Europe, aujourd’hui, la souveraineté, la démocratie et la confiance sont en danger ! » ' \
           '« Dérives collectives » Emmanuel Macron, qui a placé la première rentrée de son quinquennat sous le signe ' \
           'de l’Europe, a continué de développer sa vision d’une refonte en profondeur de l’UE. Dans un long ' \
           'discours aux allures de prêche, truffé de citations (Périclès, Hegel, Séféris), le chef de l’Etat a livré ' \
           'une analyse « sans concession » des faillites de l’Europe depuis le référendum de 2005 sur le traité ' \
           'constitutionnel qui avait vu le non l’emporter en France et aux Pays-Bas, sans qu’aucune leçon n’en ait ' \
           'été vraiment tirée. « L’Europe a avancé comme à l’abri... '


def test_text_analyzer(text):
    ta = TextAnalyzer(text)
