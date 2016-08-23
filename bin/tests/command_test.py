import os, unittest

class SqliteTest(unittest.TestCase):
    def test_command(self):
        print(os.path.join(os.path.dirname(__file__), 'testing_dir'))
        os.system('python ../diary generate sqlite %s/log.sqlite3' % os.path.join(os.path.dirname(__file__), 'testing_dir'))
        self.assertTrue(os.path.exists('testing_dir/log.sqlite3'))

if __name__ == '__main__':
    unittest.main()

