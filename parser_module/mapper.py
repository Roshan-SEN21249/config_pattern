from pagination import PagewisePagination,SingleHitCase, YearPagination, YearAndPageWisePagination
from extractor import LXMLBaseExtractor, JSONBaseExtractor

PAGINATION_MAPPER = {
    0: SingleHitCase,
    1: PagewisePagination,
    2: YearPagination,
    4: YearAndPageWisePagination
}

EXTRACTOR_MAPPER = {
    0: JSONBaseExtractor,
    1: LXMLBaseExtractor,
}

