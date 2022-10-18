#from pagination_mod.base_class_implementation import BaseImplementation
from datetime import datetime


class YearPagination(BaseImplementation):
    def __init__(self,pagination_config):
        self.pagination_config = pagination_config

    def get_end(self):
        year = datetime.now().year
        return max(self.pagination_config.get('pagination_config').get('pagination').get('end_year', year), year + 1)

    def get_start(self):
        return self.pagination_config.get('pagination_config').get('pagination').get('start_year', 0)


