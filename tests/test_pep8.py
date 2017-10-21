import os
import os.path
import unittest
import pep8


class TestPep8(unittest.TestCase):

    def test_pep8(self):
        style = pep8.StyleGuide(quiet=True)
        style.options.ignore += ('E501', 'E266')
        style.options.exclude += ('.git',
                                  'requirements.txt',
                                  'circle.yml',
                                  'setup.cfg')
        style.options.statistics = True

        errors = style.check_files(get_all_python_files()).total_errors
        self.assertEqual(errors, 0, 'PEP8 style errors: %d' % errors)


def get_all_python_files():
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(
            os.getcwd()) for f in filenames if os.path.splitext(f)[1] == '.py']
