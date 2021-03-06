#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Logging snippet based on Sam & Max's.

import logging
import re
from logging import FileHandler


class Logger:
    LOG_TYPES_DICT = {
        'INFO_DOC_UPDATE_SUCCESS': 'Document with URL %{url} is successfully updated.',
        'INFO_DOC_ALREADY_UPTODATE': 'Document with URL %{url} exists and is already up-to-date.',
        'INFO_DOC_STORE_SUCCESS': 'Document with URL %{url} is successfully indexed.',
        'WARN_DOC_DELETED': 'Document "%{doc_id}" with URL %{url} is deleted.',
        'WARN_DOMAIN_MALFORMED': 'Domain of URL %{url} is malformed.',
        'WARN_DOMAIN_NOT_SUPPORTED': 'Domain %{domain} is currently not supported.',
        'WARN_URL_NOT_ARTICLE': 'URL %{url} (redirecting to %{final_url}) does not correspond to '
                                'article format for this website.',
        'WARN_CONTENT_NOT_SUPPORTED': 'Content in URL %{url} (redirecting to %{final_url}) is not supported.',
        'INFO_DOC_NOT_CHANGED': 'Document "%{doc_id}" with URL %{url} did not change after revision.',
        'WARN_ATTRIBUTE_PARSING_ERROR': 'Extraction of "%{attribute}" attribute for URL %{url} failed :'
                                        ' %{error_message}',
        'WARN_MANDATORY_PARSING_ERROR': 'Extraction of mandatory "%{attribute}" attribute for URL'
                                        ' %{url} failed : %{error_message}',
        'INFO_FEED_STORE_SUCCESS': 'Feed %{feed_url} was successfully indexed.',
        'INFO_FEED_UPDATE_SUCCESS': 'Feed %{feed_url} was successfully updated.',
        'INFO_FEED_HARVEST_END': 'Feed %{feed_url} gathered %{gathered} documents on %{total} (%{existed} '
                                 'already up-to-date, %{domain_unsupported} which domain was not supported, '
                                 '%{url_unsupported} which URL was not supported, %{not_article} which were not articles,'
                                 '%{errors} whose parsing failed), and recursively gathered %{i_gathered} links on '
                                 '%{i_total} (%{i_existed} already up-to-date, %{i_d_unsupported} which domain '
                                 'was not supported, %{i_a_unsupported} which URL '
                                 'was not supported, %{i_not_article} which were not articles, and '
                                 '%{i_errors} whose parsing failed)',
        'INFO_LIST_HARVEST_END': 'Provided URL list gathered %{gathered} documents on %{total} (%{existed} '
                                 'already up-to-date, %{domain_unsupported} which domain was not supported, '
                                 '%{url_unsupported} which URL was not supported, %{not_article} which were not articles,'
                                 '%{errors} whose parsing failed), and recursively gathered %{i_gathered} links on '
                                 '%{i_total} (%{i_existed} already up-to-date, %{i_d_unsupported} which domain '
                                 'was not supported, %{i_a_unsupported} which URL '
                                 'was not supported, %{i_not_article} which were not articles, and %{i_errors} whose parsing failed)',
        'INFO_SOURCE_HARVEST_END': 'For media %{media_name}, %{gathered} documents were gathered on %{total} (%{existed} '
                                 'already up-to-date, %{domain_unsupported} which domain was not supported, '
                                 '%{url_unsupported} which URL was not supported, %{not_article} which were not articles,'
                                 '%{errors} whose parsing failed), and recursively gathered %{i_gathered} links on '
                                 '%{i_total} (%{i_existed} already up-to-date, %{i_d_unsupported} which domain '
                                 'was not supported, %{i_a_unsupported} which URL '
                                 'was not supported, %{i_not_article} which were not articles, and '
                                 '%{i_errors} whose parsing failed)',
        'WARN_URL_INVALID': 'URL %{url} is invalid.',
        'WARN_FEED_UNAVAILABLE': 'Feed %{url} is unavailable with error code %{status}.'
    }
    LOG_TYPES = LOG_TYPES_DICT.keys()

    def __init__(self):
        # création de l'objet logger qui va nous servir à écrire dans les logs
        self.logger = logging.getLogger(__name__)
        # on met le niveau du logger à DEBUG, comme ça il écrit tout
        self.logger.setLevel(logging.DEBUG)

        # Shut up, elastic 404's
        logging.getLogger('elasticsearch').setLevel(logging.ERROR)

        # création d'un formateur qui va ajouter le temps, le niveau
        # de chaque message quand on écrira un message dans le log
        formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
        # création d'un handler qui va rediriger une écriture du log vers
        # un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
        file_handler = FileHandler('activity.log', 'a')

        # on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
        # créé précédement et on ajoute ce handler au logger
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # création d'un second handler qui va rediriger chaque écriture de log
        # sur la console
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        self.token_regex = re.compile(r'%{\w+}')

    def log(self, log_type: str, *args):
        if log_type not in self.LOG_TYPES:
            raise ValueError
        log_message = self.LOG_TYPES_DICT[log_type]
        level = logging.getLevelName(log_type[:4])
        msg = log_type[5:] + " :: " + self.token_regex.sub('%s', log_message)

        self.logger.log(level, msg, *args)


logger = Logger()
