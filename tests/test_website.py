#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from sites.website import Website
from tests.mocks.fake_website import FakeWebsite
from tests.mocks.data_access import MockedDataAccess


class WebsiteTests(unittest.TestCase):

    @patch('sites.website.DataAccess', new=MockedDataAccess)
    def test_execute_returns_report_of_type_dict(self):
        _fake_website = FakeWebsite(False)
        result = _fake_website.execute()
        self.assertEquals(type(result), dict)
        self.assertEquals(result,
                          {'url': 'fakewebsite.com',
                           'products_found': 0,
                           'new_products_found': 0,
                           'runtime': '0:00:00'})

    @patch('sites.website.DataAccess')
    def test_execute_not_scrape_existing_product_urls(
            self, mocked_data_access):
        existing_products = ['www.some_product.com/123']
        mocked_data_access = MockedDataAccess(False)
        mocked_data_access.set_existing_products(existing_products)

        _fake_website = FakeWebsite(False)
        _fake_website.set_product_urls(existing_products)
        result = _fake_website.execute()
        self.assertEquals(result['products_found'], 1)
        self.assertEquals(result['new_products_found'], 0)
        self.assertFalse(mocked_data_access.save_products_invoked)
        self.assertTrue(mocked_data_access.filter_existing_products)

if __name__ == '__main__':
    unittest.main()


# happy path
# site not found
# no urls found
# no new products found
# run time calculated
# test for dry run
# error thrown
