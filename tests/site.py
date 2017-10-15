import unittest


class SiteTests(unittest.TestCase):
    def test_pass(self):
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
