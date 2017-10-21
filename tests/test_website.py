#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from sites.website import Website
from tests.mocks.fake_website import FakeWebsite
from tests.mocks.data_access import MockedDataAccess


class WebsiteTests(unittest.TestCase):

    @patch('components.data_access.data_access.DataAccess', new=MockedDataAccess)
    def test_execute_returns_report_of_type_dict(self):
        _fake_website = FakeWebsite(False)
        _fake_website.execute()

if __name__ == '__main__':
    unittest.main()


# happy path
# site not found
# no urls found
# no new products found
# run time calculated
# test for dry run
# error thrown
