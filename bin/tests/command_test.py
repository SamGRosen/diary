import os, unittest

class SqliteTest(unittest.TestCase):
    def test_command(self):
        os.system('python ../diary generate sqlite')
        self.assertTrue(os.path.exists('log.sqlite3'))

if __name__ == '__main__':
    unittest.main()

