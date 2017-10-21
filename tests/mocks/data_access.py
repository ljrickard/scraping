
class MockedDataAccess():

    def __init__(self, dry_run=False):
        self.existing_products = []
        self.save_products_invoked = False
        self.filter_existing_products_invoked = False
        self.get_product_template_invoked = False

    def get_product_template(self):
        self.get_product_template_invoked = True

    def filter_existing_products(self, arg1, arg2):
        self.filter_existing_products = True
        return self.existing_products

    def set_existing_products(self, existing_products):
        self.existing_products = existing_products

    def save_products(self):
        self.save_products_invoked = True
