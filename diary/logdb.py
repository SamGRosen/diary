import sqlite3
import os, sys


class DiaryDB(object):
    """
    DiaryDB is meant to be an easy way to log events into a database.
    DiaryDB should be inherited from and create_table and log should
    be overridden in such a way to store an event in the database.
    DiaryDB.log must take a first argument that is an event with information
    to log. DiaryDB uses SQLite3.
    """

    def __init__(self, path=None):
        """
        Create the connection with the database and attempt to make a table.
        :param path: relative path of database
        """
        if path is None:
            if sys.argv[0]:
                self.path = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'log.sqlite3')
            else:
                self.path = 'log.sqlite3'
        else:
            self.path = path
        self.conn = sqlite3.connect(self.path, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """
        Create tables to accommodate an event class
        """
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS logs
                (inputDT TIMESTAMP, level TEXT, log TEXT)
                            ''')

    def log(self, event):
        """
        Log an event into the database. Automatically commits executions.
        The base log method is fit for the base event class.

        :param event: event object to commit to db
        """
        try:
            with self.conn:
                self.cursor.execute('''
                                    INSERT INTO logs(inputDT, level, log)
                                                     VALUES(?, ?, ?)''',
                                    (event.dt, event.level_str, event.info))
        except sqlite3.ProgrammingError:
            raise ValueError("""diary does not support logging unicode strings into a database in ython2.
    To avoid this:
        1. Ensure your strings are converted to the 'str' type before logging
        2. Write your own implementation of DiaryDB that can handle unicode
            """)

    def assert_event_logged(self, log, level='%', limit=-1):
        """Testing method to ensure an event is logged

        :param log: log text to look
        :param level: info text to look for - % for any level
        :param limit: how far back to look in logs
        :asserts: if an event with given parameters is logged
        """
        entries = self.cursor.execute('''
            SELECT * FROM logs WHERE log=(?) AND level LIKE (?) ORDER BY
            inputDT ASC LIMIT (?)''', (log, level, limit))
        assert bool(entries.fetchone())

    def close(self):
        """Close the connection"""
        try:
            self.conn.close()
        except sqlite3.ProgrammingError:
            pass

    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
