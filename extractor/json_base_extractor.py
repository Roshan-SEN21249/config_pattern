import json
from datetime import datetime
from dateutil.parser import parse
parser_schema_who = {
    'rows': 'value',
    'attributes': {
        'link': {
            'key': 'DownloadUrl',
        },
        'title': {
            'key': 'Title'
        },
        'date': {
            'key': 'FormatedDate',
            'date_format': '%d %B %Y',
        },
        'extras':{
            'key': ['ItemDefaultUrl', 'Tag','ThumbnailUrl', 'TrimmedTitle']

        }
    }
}

key_mapper = {
    'date_format': 'attributes.date.date_format',
    'rows': 'rows',
    'link': 'attributes.link.key',
    'title': 'attributes.title.key',
    'date': 'attributes.date.key',
    'extras': 'attributes.extras.key',
    'link_filter': 'attributes.link.filter',
    'title_filter': 'attributes.title.filter',
    'date_filter': 'attributes.title.filter',
}


def get_attribute_key(attribute_name, data):
    if attribute_name not in key_mapper.keys():
        return ''
    paths = key_mapper.get(attribute_name, []).split('.')
    for path in paths:
        data = data.get(path, {})
        if not data:
            return ''
    return data


class JSONBaseExtractor:
    json_root = None
    parser_schema = None
    response = None
    date_string_format = None
    base_url = None
    path = None

    def __init__(self, response, parser_schema=None, base_url=None):
        self.response = response
        self.parser_schema = parser_schema
        self.base_url = base_url
        try:
            self.json_root = json.loads(response.content)
        except Exception as e:
            print("error while making root exception {}".format(e))

    def filter_rows(self, rows):
        return rows

    def get_value(self, key, parser_schema, data):
        paths = get_attribute_key(key, parser_schema).split('.')
        if paths and paths[0] == '':
            return data
        for path in paths:
            if path in data.keys():
                data = data.get(path, dict())
        return data

    def get_rows(self, json_root, parser_schema):
        main_data_path = get_attribute_key('main_div', parser_schema)
        main_data = self.get_value(main_data_path, parser_schema, self.json_root) if main_data_path else None
        # main_data = main_data if main_data else json_root
        rows = self.get_value('rows', parser_schema, main_data if main_data else json_root)
        rows = self.filter_rows(rows)
        return rows

    def get_extras(self, row, parser_schema):
        #extras_list = ['ItemDefaultUrl', 'Tag','ThumbnailUrl', 'TrimmedTitle']
        extras_attributes = get_attribute_key('extras',parser_schema)
        extras = dict()
        for key in row.keys():
            if key in extras_attributes:
                extras[key] = row.get(key)
        return extras

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

    def extract_utility(self, rows,parser_schema, rv):
        for row in rows:
            rv['links'].append(self.get_value('link',parser_schema, row))
            rv['titles'].append(self.get_value('title',parser_schema, row))
            rv['dates'].append(self.get_datetime_object(self.get_value('date',parser_schema, row)))
            rv['extras'].append(self.get_extras(row,parser_schema))

    def extract(self):
        rv = {"links": [], "dates": [], "titles": [], "extras": []}
        json_root = self.json_root
        if not json_root:
            return rv
        parser_schema = self.parser_schema
        self.date_string_format = get_attribute_key('date_format', parser_schema)
        rows = self.get_rows(json_root, parser_schema)
        self.extract_utility(rows, parser_schema,rv)
        return rv

