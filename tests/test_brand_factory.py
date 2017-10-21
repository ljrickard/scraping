#!/usr/bin/env python3
import unittest
from sites.brand_factory import Brands
from sites.website import Website


class BrandsTests(unittest.TestCase):

    def test_brand_factory_should_return_type_website(self):
        self.assertTrue(isinstance(Brands(True).factory('kiehls'), Website))

    def test_brand_factory_should_rasie_value_error_if_brand_not_found(self):
        with self.assertRaises(ValueError):
            Brands(True).factory('no_brand')


if __name__ == '__main__':
    unittest.main()
