import os, sys
import unittest


class SqliteTest(unittest.TestCase):
    TESTING_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'testing_dir'))

    def test_command(self):
        command = 'diary generate sqlite %s/log.sqlite3' % self.TESTING_DIR
        os.system(command)

        self.assertTrue(os.path.exists(os.path.join(self.TESTING_DIR, 'log.sqlite3')))

    def test_command_no_path_given(self):
        command = 'diary generate sqlite'
        os.system(command)
        target_path = os.path.join(os.getcwd(), 'log.sqlite3')
        self.assertTrue(os.path.exists(target_path))
        os.remove(target_path)

    def test_command_specific_name_given(self):
        command = 'diary generate sqlite mylog.sqlite3'
        os.system(command)
        target_path = os.path.join(os.getcwd(), 'mylog.sqlite3')
        self.assertTrue(os.path.exists(target_path))
        os.remove(target_path)

    def test_command_weird_extension(self):
        command = 'diary generate sqlite mylog.diary.log'
        os.system(command)
        target_path = os.path.join(os.getcwd(), 'mylog.diary.log')
        self.assertTrue(os.path.exists(target_path))
        os.remove(target_path)

if __name__ == '__main__':
    unittest.main()

