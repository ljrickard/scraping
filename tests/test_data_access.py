#!/usr/bin/env python3
import unittest
from components.data_access.data_access import DataAccess


class DataAccessTests(unittest.TestCase):

    def setUp(self):
        self.data_access = DataAccess()


if __name__ == '__main__':
    unittest.main()


# https://stackoverflow.com/questions/3829742/assert-that-a-method-was-called-in-a-python-unit-test
