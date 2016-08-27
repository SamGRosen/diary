import os
import unittest


class SqliteTest(unittest.TestCase):
    TESTING_DIR = os.path.join(os.path.dirname(__file__), 'testing_dir')

    def test_command_and_logdb_defaults(self):
        command = 'diary generate sqlite %s/log.sqlite3' % self.TESTING_DIR
        os.system(command)

        self.assertTrue(os.path.exists(os.path.join(self.TESTING_DIR, 'log.sqlite3')))

if __name__ == '__main__':
    unittest.main()

