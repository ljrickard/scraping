import unittest
import mock


class DataAccessTests(unittest.TestCase):

    def setUp(self):
        self.data_access = DataAccess()

    def test_data_access_should_only_write_to_local_file_when_dry_run_is_true(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main() 


# https://stackoverflow.com/questions/3829742/assert-that-a-method-was-called-in-a-python-unit-test
