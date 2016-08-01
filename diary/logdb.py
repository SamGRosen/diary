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

    def log(self, event):
        if type(event.level) is FunctionType:
            level_text = event.level.__name__.upper()
        else:
            level_text = str(event.level)
        self.cursor.execute('''
                            INSERT INTO logs(inputDT, level, log)
                                             VALUES(?, ?, ?)''',
                            (event.dt, level_text, event.info))

if __name__ == '__main__':
    pass
