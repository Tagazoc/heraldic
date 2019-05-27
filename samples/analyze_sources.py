from heraldic.models.document import Document
import heraldic.store.index_searcher as i_s
from heraldic.misc.functions import get_domain
import heraldic.misc.exceptions as ex
from heraldic.media.known_media import known_media

models = i_s.search_models(sort='doc_publication_time:desc', terminate_after='100000')

medias_sources = {}
medias_count = {}

for model in models:
    try:
        medias_count[model.media.value] += 1
    except KeyError:
        medias_count[model.media.value] = 1
    for url in model.href_sources.value:
        try:
            source = get_domain(url, do_not_log=True)
        except ex.InvalidUrlException:
            # Invalid URL
            continue
        try:
            source = known_media.get_media_class_by_domain(source, is_subdomain=True, log_failure=True).id
        except ex.DomainNotSupportedException:
            continue
        try:
            medias_sources[model.media.value][source] += 1
        except KeyError:
            try:
                medias_sources[model.media.value][source] = 1
            except KeyError:
                medias_sources[model.media.value] = {source: 1}

medias = list(medias_sources.keys())
for media in medias:
    media_map = map(lambda t: str(medias_sources[media][t]) if t in medias_sources[media].keys() else '0', medias)
    print(",".join(media_map))
