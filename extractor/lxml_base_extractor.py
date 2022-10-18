import re

from dateutil.parser import parse
from lxml.html import document_fromstring
from datetime import datetime

# famhp
# https://www.famhp.be

parser_schema_famhp = {
    'main_div': './/div[@class="view__content"]',
    'rows': './/div[@class="view__row"]',
    'attributes': {
        'link': {
            'xpath': './/span[@class="field-content"]//@href',
        },
        'title': {
            'xpath': './/span[@class="field-content"]//a'
        },
    }
}

# bls
# https://www.bls.gov

parser_schema_bls = {
    'attributes': {
        'link': {
            'xpath': './/li//a//@href',
            'filter': '.*\.pdf'
        },
    }
}

xpath_map = {
    'date_format': 'attributes.date.date_format',
    'main_div': 'main_div',
    'rows': 'rows',
    'link': 'attributes.link.xpath',
    'title': 'attributes.title.xpath',
    'date': 'attributes.date.xpath',
    'extras': 'attributes.extras.xpath',
    'link_filter': 'attributes.link.filter',
    'title_filter': 'attributes.title.filter',
    'date_filter': 'attributes.title.filter',
}


def get_xpath(key, data):
    if key not in xpath_map.keys():
        return ''
    paths = xpath_map.get(key, []).split('.')
    for path in paths:
        data = data.get(path, {})
        if not data:
            return ''
    return data


class LXMLBaseExtractor:
    root = None
    parser_schema = None
    response = None
    date_string_format = None
    base_url = None

    def __init__(self, response, parser_schema=None, base_url=None):
        self.response = response
        self.parser_schema = parser_schema
        self.base_url = base_url
        try:
            self.root = document_fromstring(self.response.content)
        except Exception as e:
            print("error while making root exception {}".format(e))

    def filter_rows(self, rows):
        return rows

    def get_rows(self, root, parser_schema):
        main_div_xpath = get_xpath('main_div', parser_schema)
        main_div = root.xpath(main_div_xpath) if main_div_xpath else None
        main_div = main_div[0] if main_div else root
        rows = main_div.xpath(get_xpath('rows', parser_schema))
        rows = self.filter_rows(rows)
        return rows

    def get_link(self, xpath_to_link='', row=None, anchor_tag=None):
        link = ''
        if not anchor_tag:
            link = row.xpath(xpath_to_link)
        return link[0] if link else None

    def get_title(self, xpath_to_title='', row=None):
        if not xpath_to_title:
            return None
        title_tag = row.xpath(xpath_to_title)
        return title_tag[0].text if title_tag else None

    def get_datetime_object(self, date_string, parse_flag=True):
        date_obj = datetime.now()
        if not date_string:
            return date_obj
        elif self.date_string_format:
            try:
                date_obj = datetime.strptime(date_string, self.date_string_format)
            except Exception as e:
                pass
        elif parse_flag:
            date_obj = parse(date_string)
        return date_obj

    def add_base_url(self, links):
        return [self.base_url + link if 'http' not in link else link for link in links]

    def get_date(self, xpath_to_date='', row=None):
        if not xpath_to_date:
            return None
        date_tag = row.xpath(xpath_to_date)
        return self.get_datetime_object(date_tag[0].text) if date_tag else None

    def get_all_links(self, rows, parser_schema, rv):
        # print("get_all_links total rows:: {}".format(len(rows)))
        xpath_to_link = get_xpath('link', parser_schema)
        # print("link xpath::: ", xpath_to_link)
        if not xpath_to_link:
            return
        links = rv.get('links')
        if not rows:
            links = self.root.xpath(xpath_to_link)
        else:
            for i, row in enumerate(rows):
                link = self.get_link(xpath_to_link, row)
                links.append(link)
        rv['links'] = self.add_base_url(links)
        return

    def get_all_titles(self, rows, parser_schema, rv):
        print("get_all_titles total rows:: {}".format(len(rows)))
        xpath_to_title = get_xpath('title', parser_schema)
        print("link xpath::: ", xpath_to_title)
        if not xpath_to_title:
            return
        titles = rv.get('titles')
        for row in rows:
            titles.append(self.get_title(xpath_to_title, row))
        rv['titles'] = titles

    def get_all_dates(self, rows, parser_schema, rv):
        xpath_to_date = get_xpath('date', parser_schema)
        if not xpath_to_date:
            return
        dates = rv.get('dates')
        for i, row in enumerate(rows):
            dates.append(self.get_date(xpath_to_date, row))
        rv['dates'] = dates

    def get_all_extras(self, rows, parser_schema, rv):
        pass

    def extract_utility(self, rows, parser_schema, rv):
        self.get_all_links(rows, parser_schema, rv)
        if not rows:
            return
        self.get_all_titles(rows, parser_schema, rv)
        self.get_all_dates(rows, parser_schema, rv)
        self.get_all_extras(rows, parser_schema, rv)

    def get_default_return_dict(self):
        return {"links": [], "dates": [], "titles": [], "extras": []}

    def add_index(self,index, rv,final_dict):
        for key in ['links','dates','titles']:
            if index < len(rv[key]):
                final_dict[key].append(rv[key][index])

    def filter_meta_data(self, rv, final_dict):
        link_filter_regex = get_xpath('link_filter', self.parser_schema)
        if not link_filter_regex:
            return rv
        links = rv.get('links')
        for index,link in enumerate(links):
            if re.search(link_filter_regex,link):
                self.add_index(index,rv,final_dict)
        return final_dict

    def extract(self):
        rv = {"links": [], "dates": [], "titles": [], "extras": []}
        root = self.root
        if not root:
            return rv
        parser_schema = self.parser_schema
        self.date_string_format = get_xpath('date_format', parser_schema)
        rows = self.get_rows(root, parser_schema) if 'main_div' in parser_schema.keys() else None
        self.extract_utility(rows, parser_schema, rv)
        final_dict = self.get_default_return_dict()
        self.filter_meta_data(rv, final_dict)
        return rv
