# from pagination_mod.base_class import BasePagination


class BaseImplementation(BasePagination):
    pagination_config = None

    def __init__(self, pagination_config):
        self.pagination_config = pagination_config

    def get_scrape_url(self):
        return self.pagination_config.get('pagination_config',{}).get('scrape_url', '')

    def get_single_hit_flag(self):
        return self.pagination_config.get('pagination_config',{}).get('single_hit_case_flag', False)

    def get_data(self, **kwargs):
        string_data = self.pagination_config.get('pagination_config',{}).get('data', '')
        return string_data.format(kwargs)

    def get_loop_flag(self):
        return -1 if self.pagination_config.get('pagination_config').get('pagination').get('yearwise', False) else 1

    def get_iterator(self):
        scrape_url = self.get_scrape_url()
        start = self.get_start()
        end = self.get_end()
        loop_direction_value = self.get_loop_flag()
        for i in range(start, end)[::loop_direction_value]:
            l = scrape_url
            data = self.get_data(**{'i': i})
            yield {'next_scrape_url': l.format(i), 'data': data}
