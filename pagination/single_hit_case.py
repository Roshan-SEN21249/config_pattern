from base_class_implementation import BaseImplementation


class SingleHitCase(BaseImplementation):

    def get_iterator(self):
        yield self.get_scrape_url()

