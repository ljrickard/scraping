from sites.website import Website


class FakeWebsite(Website):

BASE_URL = "fakewebsite.com"
BRAND = "FakeWebsite"

    def __init__(self, dry_run):
        super(FakeWebsite, self).__init__(dry_run)
        self.base_url = BASE_URL
        self.brand = BRAND

    def execute(self):
        return super(FakeWebsite, self).execute()

    def get_product_urls(self):
        return []

    def scrape_product_urls(self, product_urls):
        pass
