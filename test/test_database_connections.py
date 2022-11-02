""" testing database connection. """
import pathlib
import unittest

from singletons.resources import Resources


class MyTestCase(unittest.TestCase):
    """ Test connectivity and stuff like that """

    def test_find_one(self):
        """ the connection works if data can be received. """
        files = 'files/config.json'
        templates = 'templates'
        if not pathlib.Path(files).exists():
            files = '../' + files
            templates = '../' + templates
        db = Resources(files, templates).db_admin
        item: dict = db.get_collection('scopes').find_one({})
        assert item is not None


if __name__ == '__main__':
    unittest.main()
