from __future__ import absolute_import
from bin import diary
import os
import unittest


class SqliteTest(unittest.TestCase):
    TESTING_DIR = os.path.join(os.path.dirname(__file__), 'testing_dir')

    def test_command(self):
        print(os.path.join(os.path.dirname(__file__), 'testing_dir'))
        command = 'python ../diary.py generate sqlite %s/log.sqlite3' % self.TESTING_DIR
        args = command.split()
        diary.diary(args=args)

        self.assertTrue(os.path.exists('testing_dir/log.sqlite3'))

if __name__ == '__main__':
    unittest.main()

