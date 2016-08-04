import sqlite3
from types import FunctionType


class LoggerDB():
    """
    LoggerDB is meant to be an easy way to log events into a database.
    LoggerDB should be inherited from and create_table and log should
    be overridden in such a way to store an event in the database.
    LoggerDB.log must take a first argument that is an event with information
    to log.
    """

    def __init__(self, path):
        """
        Create the connection with the databse and attempt to make a table.
        :param path: relative path of database
        """
        self.conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """
        Create a table to accomodate an event class. Attempts to create
        the table but if the table already exists the program continues.

        """
        self.cursor.execute('''
                CREATE TABLE logs (inputDT TIMESTAMP, level TEXT, log TEXT)
            ''')

    def log(self, event):
        """
        Log an event into the database. Automatically commits executions.
        The base log method is fit for the base event class.

        :param event: event object to commit to db
        """
        if type(event.level) is FunctionType:
            level_text = event.level.__name__.upper()
        else:
            level_text = str(event.level)
        with self.conn:
            self.cursor.execute('''
                                INSERT INTO logs(inputDT, level, log)
                                                 VALUES(?, ?, ?)''',
                                (event.dt, level_text, event.info))
