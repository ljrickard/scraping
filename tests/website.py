import unittest
from sites.website import Website


class WebsiteTests(unittest.TestCase):
    def test_execute_returns_report_of_type_dict(self):
        self.assertTrue(True)

    def test_fail(self):
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()

# happy path
# site not found
# no urls found
# no new products found
# run time calculated
# test for dry run
# error thrown
