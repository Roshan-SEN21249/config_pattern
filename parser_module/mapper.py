# from config_pattern.pagination.pagewise import PagewisePagination
# from config_pattern.pagination.yearwise import YearPagination
# from config_pattern.pagination.single_hit_case import SingleHitCase
# from config_pattern.pagination.year_and_pagewise import YearAndPageWisePagination
# from config_pattern.extractor.json_base_extractor import JSONBaseExtractor
# from config_pattern.extractor.lxml_base_extractor import LXMLBaseExtractor

from pagination.pagewise import PagewisePagination
from pagination.yearwise import YearPagination
from pagination.single_hit_case import SingleHitCase
from pagination.year_and_pagewise import YearAndPageWisePagination
from extractor.json_base_extractor import JSONBaseExtractor
from extractor.lxml_base_extractor import LXMLBaseExtractor

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

