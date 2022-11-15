from parser_module.mapper import PAGINATION_MAPPER, EXTRACTOR_MAPPER
from response_module.response_handler import Response
from parser_module.temp_doc import tempDocument
from lxml.html import document_fromstring, tostring

TEMP_DOCS_LIST = []


class Parser:
    def __init__(self, source_config):
        self.source_config = source_config
        self.parser_schema = self.source_config.get('parser_schema', dict())
        self.urls_config = self.source_config.get('urls_config', dict())
        self.pagination_config = self.source_config.get('pagination_config', dict())
        self.response_config = self.source_config.get('response_config', {})

    def get_response(self, url):
        print("getting the reponse for the url  {}".format(url))
        rp = Response(self.source_config)
        response_obj = rp.get_response(url)
        # response_obj = get(url)
        print("got {}".format(response_obj.status_code))
        return response_obj

    def get_pagination_obj(self):
        return PAGINATION_MAPPER.get(self.pagination_config.get('type', 0))(self.pagination_config)

    def extract_meta_data(self, response=None):
        ext_obj = EXTRACTOR_MAPPER.get(1)(response, self.parser_schema, self.urls_config.get('base_url', ''))
        return ext_obj.extract()

    def create_temp_objects(self, meta_dict):
        total_docs = []
        links = meta_dict.get('links', [])
        titles = meta_dict.get('titles', [])
        dates = meta_dict.get('filing_date', [])
        extras = meta_dict.get('extras', [])
        titles_len, dates_len, extras_len = len(titles), len(dates), len(extras)
        for index, link in enumerate(links):
            title = titles[index] if index < titles_len else None
            date = dates[index] if index < dates_len else None
            extra = titles[index] if index < extras_len else None
            temp_doc = tempDocument(link, date, title, extra)
            total_docs.append(temp_doc)
        return total_docs

    def analyser(self):
        print("analyser_st ....................")
        pg_obj = self.get_pagination_obj()
        if not pg_obj:
            print("No pagination object")
            return
        iterator_obj = pg_obj.get_iterator()
        try:
            while True:
                url_dict = iterator_obj.next()
                print(url_dict)
                response = self.get_response(url_dict.get('next_scrape_url'))
                meta_data_dict = self.extract_meta_data(response)
                # push  meta data_dict to the META_DATA_QUEUE
                TEMP_DOCS_LIST.append(self.create_temp_objects(meta_data_dict))
        except Exception as e:
            print(e)
            print("exception ....................")
        return TEMP_DOCS_LIST


class SimpleXpathContentParser:
    def __init__(self, parse_config):
        self.parse_config = parse_config
        self.content_config = self.parse_config.get('content_config')
        self.xpath_to_main_content = self.content_config.get('main_content').get('xpath')

    def get_main_content(self, root):
        main_content = root.xpath(self.xpath_to_main_content)  # todo
        if main_content:
            return tostring(main_content[0]).decode('utf-8')
        return ''

    def get_title(self, root):
        pass

    def get_date(self, root):
        pass

    def populate_meta_data(self):
        pass

    def populate_content(self, root):
        pass


class SimpleXpathContentDateParser(SimpleXpathContentParser):
    def __init__(self, parse_config):
        self.parse_config = parse_config
        self.content_config = self.parse_config.get('content_config')
        self.xpath_to_main_content = self.content_config.get('main_content').get('xpath')

    def get_date(self, root):
        pass

    def populate_meta_data(self):
        pass


class SimpleXpathContentTitleDateParser(SimpleXpathContentParser):
    def __init__(self, parse_config):
        self.parse_config = parse_config
        self.content_config = self.parse_config.get('content_config')
        self.xpath_to_main_content = self.content_config.get('main_content').get('xpath')

    def get_date(self, root):
        pass

    def get_title(self, root):
        pass

    def populate_meta_data(self):
        pass