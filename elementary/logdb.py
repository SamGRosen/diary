import sqlite3
from datetime import datetime as dt
from types import FunctionType


class LoggerDB():

    def __init__(self, path):
        self.conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute('''
                                CREATE TABLE logs
                                    (inputDT DATE, level TEXT, log TEXT)
                                ''')
        except sqlite3.OperationalError:
            pass

    def log(self, text, level):
        if type(level) is FunctionType:
            level_text = level.__name__.upper()
        else:
            level_text = str(level)
        self.cursor.execute('''
                            INSERT INTO logs(inputDT, level, log)
                                             VALUES(?, ?, ?)''',
                            (dt.now(), level_text, text))

if __name__ == '__main__':
    pass
