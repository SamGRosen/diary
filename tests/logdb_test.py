from diary import DiaryDB, Event
import unittest
import sqlite3
import os.path


class TestDiaryDB(unittest.TestCase):
    TEMP_DB_PATH = os.path.join(os.path.dirname(__file__),
                                 'testing_dir', 'temp.db')
    SIMPLE_EVENT = Event("INFO", "LEVEL")

    def setUp(self):
        self.logdb = DiaryDB(self.TEMP_DB_PATH)

    @classmethod
    def tearDownClass(cls):
        import os
        os.remove(cls.TEMP_DB_PATH)

    def constructs_correctly(self):
        self.assertIsInstance(self.logdb.conn, sqlite3.Connection)
        self.assertIsInstance(self.logdb.cursor, sqlite3.Cursor)

    def test_creates_table(self):
        table = self.logdb.cursor.execute('''SELECT name FROM sqlite_master
                                             WHERE type="table" AND name="logs"
                                          ''').fetchone()[0]
        self.assertEquals(table, 'logs')

    def test_creates_table_already_exists(self):
        self.logdb.create_tables()
        tables = self.logdb.cursor.execute('''SELECT name FROM sqlite_master
                                              WHERE type="table" AND name="logs"
                                           ''').fetchall()
        self.assertEquals(len(tables), 1)

    def test_log(self):
        self.logdb.log(self.SIMPLE_EVENT)
        entry = self.logdb.cursor.execute('''SELECT * FROM logs ORDER BY
                                             inputDT ASC LIMIT 1''').fetchone()
        self.assertEquals(entry[0], self.SIMPLE_EVENT.dt)
        self.assertEquals(entry[1], self.SIMPLE_EVENT.level)
        self.assertEquals(entry[2], self.SIMPLE_EVENT.info)

    def test_close(self):
        self.logdb.close()
        with self.assertRaises(sqlite3.ProgrammingError,
                               msg="Cannot operate on a closed database."):
            self.logdb.conn.execute("SELECT 1 FROM logs LIMIT 1")

if __name__ == '__main__':
    unittest.main()
