from sites.website import Website

BASE_URL = "fakewebsite.com"
BRAND = "FakeWebsite"


class FakeWebsite(Website):

    def __init__(self, dry_run):
        super(FakeWebsite, self).__init__(dry_run)
        self.base_url = BASE_URL
        self.brand = BRAND
        self.product_urls = []

    def execute(self):
        return super(FakeWebsite, self).execute()

    def get_product_urls(self):
        return self.product_urls

    def set_product_urls(self, product_urls):
        self.product_urls = product_urls

    def scrape_product_urls(self, product_urls):
        pass
