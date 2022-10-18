from parser_module.mapper import PAGINATION_MAPPER, EXTRACTOR_MAPPER
from requests import *

META_DICT_LIST = []


class Parser:
    def __init__(self, source_config):
        self.source_config = source_config
        self.parser_schema = self.source_config.get('parser_schema', dict())
        self.urls_config = self.source_config.get('urls_config', dict())

    def get_response(self, url):
        print("getting the reponse for the url  {}".format(url))
        resp = get(url)
        print("got {}".format(resp.status_code))
        return resp

    def get_pagination_obj(self):
        pagination_config = self.source_config.get('pagination_config', dict())
        return PAGINATION_MAPPER.get(pagination_config.get('type', 0))(self.source_config)

    def extract_meta_data(self, response=None):
        ext_obj = EXTRACTOR_MAPPER.get(1)(response, self.parser_schema, self.urls_config.get('base_url', ''))
        return ext_obj.extract()

    def analyser(self):
        pg_obj = self.get_pagination_obj()
        if not pg_obj:
            return
        iterator_obj = pg_obj.get_iterator()
        try:
            while True:
                url_dict = iterator_obj.__next__()
                response = self.get_response(url_dict.get('next_scrape_url'))
                meta_data_dict = self.extract_meta_data(response)
                # push  meta data_dict to the META_DATA_QUEUE
                META_DICT_LIST.append(meta_data_dict)
        except:
            pass
        return META_DICT_LIST
