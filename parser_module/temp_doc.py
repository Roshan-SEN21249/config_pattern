class tempDocument:
    def __init__(self, link, filing_date=None, title=None, extras=None):
        self.link = link
        self.title = title
        self.filing_date = filing_date
        self.extras = extras

    def set_title(self, title):
        self.title = title

    def get_title(self):
        return self.title

    def set_filing_date(self, filing_date):
        self.filing_date = filing_date

    def get_filing_date(self):
        return self.filing_date

    def get_link(self):
        return self.link

    def get_extras(self):
        return self.extras

    def set_extras(self, extras):
        self.extras = extras
