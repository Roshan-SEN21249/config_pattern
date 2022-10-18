#from pagination_mod.base_class_implementation import BaseImplementation


class PagewisePagination(BaseImplementation):
    def __init__(self,pagination_config):
        self.pagination_config = pagination_config

    def get_start(self):
        return self.pagination_config.get('pagination_config').get('pagination').get('start_page', 0)

    def get_end(self):
        return self.pagination_config.get('pagination_config').get('pagination').get('end_page',100)
