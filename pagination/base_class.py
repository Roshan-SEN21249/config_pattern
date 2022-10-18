class BasePagination:
    pagination_config = None

    def __init__(self,pagination_config):
        self.pagination_config = pagination_config

    def get_start(self):
        pass

    def get_end(self):
        pass

    def get_scrape_url(self):
        return

    def get_single_hit_flag(self):
        pass

    def get_data(self, **kwargs):
        pass

    def get_iterator(self):
        pass
